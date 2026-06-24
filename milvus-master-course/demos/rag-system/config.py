"""RAG 知识库问答系统 - 配置管理

使用 dataclass 从环境变量和 .env 文件加载配置。
对应教程第 23 章《RAG 知识库实战》。
"""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """应用配置，所有参数均可通过环境变量覆盖"""

    # Milvus 连接
    milvus_uri: str = os.getenv("MILVUS_URI", "http://localhost:19530")
    milvus_token: str = os.getenv("MILVUS_TOKEN", "")
    collection_name: str = os.getenv("COLLECTION_NAME", "course_rag_chunks")

    # Embedding 模型（本地 sentence-transformers）
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-zh-v1.5")

    # LLM 配置（兼容 OpenAI API 格式，可对接 Ollama/vLLM 等本地服务）
    openai_base_url: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    # 文档切块参数
    # chunk_size: 每块目标字符数，中文知识库推荐 400-800
    # chunk_overlap: 相邻块重叠字符数，保证上下文衔接
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "600"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "100"))

    # 搜索参数
    top_k: int = int(os.getenv("TOP_K", "10"))
    # Rerank 后保留的文档数，进入 LLM Prompt
    rerank_top_n: int = int(os.getenv("RERANK_TOP_N", "5"))

    # API 鉴权（设置后所有写入/查询接口需携带 X-API-Key）
    api_key: str = os.getenv("API_KEY", "")

    # 日志
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
