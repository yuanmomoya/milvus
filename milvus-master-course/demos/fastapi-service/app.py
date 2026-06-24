"""FastAPI 向量搜索服务 Demo

提供 RESTful API 封装 Milvus 搜索能力，包含文档写入和语义搜索。
对应教程第 33 章《FastAPI 接口开发》。

启动方式: uvicorn app:app --reload --port 8000
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymilvus import DataType, MilvusClient
from sentence_transformers import SentenceTransformer

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)s %(name)s - %(message)s")
logger = logging.getLogger("fastapi-service")


@dataclass(frozen=True)
class Settings:
    """服务配置"""
    milvus_uri: str = os.getenv("MILVUS_URI", "http://localhost:19530")
    milvus_token: str = os.getenv("MILVUS_TOKEN", "")
    collection_name: str = os.getenv("COLLECTION_NAME", "course_search_service")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-zh-v1.5")


# ==================== 请求/响应模型 ====================

class UpsertRequest(BaseModel):
    """文档写入请求"""
    id: str
    text: str
    source: str = "api"


class SearchRequest(BaseModel):
    """搜索请求"""
    query: str
    top_k: int = Field(default=5, ge=1, le=50)
    source: str | None = None  # 可选：按来源过滤


# ==================== 初始化 ====================

settings = Settings()

# 加载 Embedding 模型（启动时一次性加载）
model = SentenceTransformer(settings.embedding_model)
dim = model.get_sentence_embedding_dimension()
if dim is None:
    raise RuntimeError("无法读取模型向量维度")

# 创建 Milvus 客户端（全局复用，内部维护连接池）
client = MilvusClient(uri=settings.milvus_uri, token=settings.milvus_token or None)
app = FastAPI(title="Milvus Search API", version="1.0.0")


def ensure_collection() -> None:
    """确保 Collection 存在且已加载"""
    if client.has_collection(settings.collection_name):
        client.load_collection(settings.collection_name)
        return
    schema = MilvusClient.create_schema(auto_id=False, enable_dynamic_field=False)
    schema.add_field("id", DataType.VARCHAR, is_primary=True, max_length=64)
    schema.add_field("text", DataType.VARCHAR, max_length=4096)
    schema.add_field("source", DataType.VARCHAR, max_length=256)
    schema.add_field("embedding", DataType.FLOAT_VECTOR, dim=dim)
    index_params = MilvusClient.prepare_index_params()
    index_params.add_index("embedding", index_type="HNSW", metric_type="COSINE", params={"M": 16, "efConstruction": 128})
    client.create_collection(settings.collection_name, schema=schema, index_params=index_params)
    client.load_collection(settings.collection_name)


def embed(texts: list[str]) -> list[list[float]]:
    """文本向量化"""
    return model.encode(texts, normalize_embeddings=True, show_progress_bar=False).astype("float32").tolist()


# ==================== API 端点 ====================

@app.on_event("startup")
def startup() -> None:
    """应用启动时初始化 Collection"""
    try:
        ensure_collection()
    except Exception:
        logger.exception("启动时初始化 Collection 失败，服务可能无法正常工作")
        raise


@app.get("/health")
def health() -> dict[str, str]:
    """健康检查"""
    return {"status": "ok"}


@app.post("/documents")
def upsert_document(payload: UpsertRequest) -> dict[str, str]:
    """写入单条文档（自动 Embedding）

    使用 upsert：相同 ID 会覆盖旧数据，保证幂等。
    """
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="text 不能为空")
    vector = embed([payload.text])[0]
    client.upsert(settings.collection_name, [{"id": payload.id, "text": payload.text, "source": payload.source, "embedding": vector}])
    return {"status": "upserted", "id": payload.id}


@app.post("/search")
def search(payload: SearchRequest) -> list[dict[str, Any]]:
    """语义搜索

    支持可选的 source 过滤，只搜索指定来源的文档。
    """
    vector = embed([payload.query])[0]
    # 构建过滤表达式（可选）
    filter_expr = f'source == "{payload.source}"' if payload.source else ""
    results = client.search(
        collection_name=settings.collection_name,
        data=[vector],
        anns_field="embedding",
        filter=filter_expr,
        search_params={"metric_type": "COSINE", "params": {"ef": 64}},
        limit=payload.top_k,
        output_fields=["text", "source"],
    )
    return [{"score": float(hit.get("distance", 0.0)), **hit.get("entity", {})} for hit in results[0]]
