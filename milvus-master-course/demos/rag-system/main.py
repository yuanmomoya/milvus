"""RAG 知识库问答系统 - FastAPI 主服务

提供文本入库和问答两个核心 API：
- POST /ingest/text: 文本切块 → Embedding → 写入 Milvus
- POST /ask: Query Rewrite → 向量召回 → Rerank → LLM 生成

对应教程第 22-25 章（RAG 架构、知识库实战、召回优化、Rerank）。
"""
from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, HTTPException
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from pydantic import BaseModel, Field

from config import Settings
from embeddings import EmbeddingService
from vector_store import Chunk, RagVectorStore

settings = Settings()
logging.basicConfig(level=settings.log_level, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
logger = logging.getLogger("rag-system")

# 初始化核心服务（应用启动时加载模型，避免每次请求重复加载）
embedding_service = EmbeddingService(settings.embedding_model)
store = RagVectorStore(settings.milvus_uri, settings.milvus_token, settings.collection_name, embedding_service.dim)
app = FastAPI(title="Milvus RAG System", version="1.0.0")


# ==================== 请求/响应模型 ====================

class IngestTextRequest(BaseModel):
    source: str = Field(..., description="文档来源标识，例如文件名或 URL")
    text: str = Field(..., description="要入库的纯文本内容")
    chunk_size: int | None = None
    chunk_overlap: int | None = None


class AskRequest(BaseModel):
    question: str
    top_k: int = 10
    history: list[dict[str, str]] = Field(default_factory=list)


class AskResponse(BaseModel):
    answer: str
    rewritten_question: str
    citations: list[dict[str, Any]]


# ==================== 核心逻辑 ====================

def split_text(text: str, source: str, chunk_size: int, chunk_overlap: int) -> list[Chunk]:
    """将长文本切块

    使用递归分割器，按中文自然边界（段落、句号等）切割，
    保证每块语义尽量完整。
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "。", "！", "？", ";", " ", ""],
    )
    chunks = splitter.split_text(text)
    return [Chunk(text=chunk, source=source, chunk_id=index) for index, chunk in enumerate(chunks)]


def rewrite_query(question: str, history: list[dict[str, str]]) -> str:
    """查询改写：结合对话历史将问题改写为独立查询

    解决多轮对话中代词指代不明的问题（如"它支持什么？"）。
    生产环境建议用 LLM 改写，这里用确定性逻辑方便无 Key 运行。
    """
    if not history:
        return question
    last_turns = " ".join(item.get("content", "") for item in history[-4:])
    return f"结合上下文：{last_turns}\n当前问题：{question}"


def rerank(question: str, docs: list[dict[str, Any]], top_n: int) -> list[dict[str, Any]]:
    """轻量 Rerank：基于字符重叠度排序

    生产环境应替换为 CrossEncoder（如 BAAI/bge-reranker-base），
    精度会显著提升。参考教程第 25 章。
    """
    q_chars = set(question.lower())
    ranked: list[dict[str, Any]] = []
    for doc in docs:
        text = str(doc.get("text", "")).lower()
        overlap = len(q_chars & set(text)) / max(len(q_chars), 1)
        ranked.append({**doc, "rerank_score": overlap})
    return sorted(ranked, key=lambda item: (item["rerank_score"], item["score"]), reverse=True)[:top_n]


def build_prompt(question: str, docs: list[dict[str, Any]]) -> str:
    """构建 RAG Prompt

    关键约束：
    1. 只基于资料回答（降低幻觉）
    2. 资料不足时明确拒答
    3. 要求标注来源编号（可追溯）
    """
    context = "\n\n".join(
        f"[来源 {index}] source={doc.get('source')} page={doc.get('page')}\n{doc.get('text')}"
        for index, doc in enumerate(docs, start=1)
    )
    return (
        "你是严谨的知识库问答助手。请只根据资料回答；"
        "如果资料不足，请说“根据现有资料无法判断”。\n\n"
        f"资料：\n{context}\n\n"
        f"问题：{question}\n\n"
        "请给出中文答案，并在关键结论后标注来源编号。"
    )


def call_llm(prompt: str) -> str:
    """调用 LLM 生成答案

    未配置 API Key 时返回检索摘要，方便本地测试召回质量。
    """
    if not settings.openai_api_key:
        return "未配置 OPENAI_API_KEY，以下是检索到的资料摘要：\n" + prompt[:1200]
    client = OpenAI(api_key=settings.openai_api_key, base_url=settings.openai_base_url)
    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,  # 低温度减少随机性，提高答案一致性
    )
    return response.choices[0].message.content or ""


# ==================== API 端点 ====================

@app.get("/health")
def health() -> dict[str, str]:
    """健康检查"""
    return {"status": "ok"}


@app.post("/ingest/text")
def ingest_text(payload: IngestTextRequest) -> dict[str, int]:
    """文本入库：切块 → Embedding → 写入 Milvus"""
    chunk_size = payload.chunk_size or settings.chunk_size
    chunk_overlap = payload.chunk_overlap or settings.chunk_overlap

    # 切块
    chunks = split_text(payload.text, payload.source, chunk_size, chunk_overlap)
    if not chunks:
        return {"chunks": 0}

    # 批量 Embedding
    vectors = embedding_service.encode([chunk.text for chunk in chunks])

    # 写入 Milvus（upsert 保证幂等）
    count = store.upsert_chunks(chunks, vectors)
    logger.info("入库完成: source=%s chunks=%d", payload.source, count)
    return {"chunks": count}


@app.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest) -> AskResponse:
    """RAG 问答：完整链路 Query Rewrite → 召回 → Rerank → 生成"""
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="question 不能为空")

    # 1. Query Rewrite（多轮对话时改写查询）
    rewritten = rewrite_query(payload.question, payload.history)

    # 2. Embedding + 向量召回
    qv = embedding_service.encode([rewritten])[0]
    recalled = store.search(qv, top_k=payload.top_k)

    # 3. Rerank 重排序（精选最相关的 N 条进入 Prompt）
    selected = rerank(rewritten, recalled, top_n=settings.rerank_top_n)

    # 4. 构建 Prompt + LLM 生成答案
    prompt = build_prompt(payload.question, selected)
    answer = call_llm(prompt)

    # 5. 返回答案和引用来源
    citations = [
        {"source": doc.get("source"), "page": doc.get("page"), "chunk_id": doc.get("chunk_id"), "score": doc.get("score")}
        for doc in selected
    ]
    return AskResponse(answer=answer, rewritten_question=rewritten, citations=citations)
