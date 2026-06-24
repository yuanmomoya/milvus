"""FastAPI 向量搜索服务 Demo

提供 RESTful API 封装 Milvus 搜索能力，包含文档写入和语义搜索。
对应教程第 33 章《FastAPI 接口开发》。

启动方式: uvicorn app:app --reload --port 8000
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymilvus import DataType, MilvusClient

# 将 milvus-master-course/ 加入搜索路径，以便导入 shared 包
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from shared.config import BaseSettings
from shared.logging_setup import configure_logging
from shared.milvus_client import build_milvus_client, hnsw_index_params
from shared.text_embedding import EmbeddingService

logger = configure_logging("fastapi-service")


@dataclass(frozen=True)
class Settings(BaseSettings):
    """服务配置"""
    collection_name: str = os.getenv("COLLECTION_NAME", "course_search_service")


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
embed_svc = EmbeddingService(settings.embedding_model)

# 创建 Milvus 客户端（全局复用，内部维护连接池）
client = build_milvus_client(settings.milvus_uri, settings.milvus_token)
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
    schema.add_field("embedding", DataType.FLOAT_VECTOR, dim=embed_svc.dim)
    index_params = MilvusClient.prepare_index_params()
    index_params.add_index(**hnsw_index_params())
    client.create_collection(settings.collection_name, schema=schema, index_params=index_params)
    client.load_collection(settings.collection_name)


# ==================== API 端点 ====================

@app.on_event("startup")
def startup() -> None:
    """应用启动时初始化 Collection"""
    ensure_collection()


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
    vector = embed_svc.encode([payload.text])[0]
    client.upsert(settings.collection_name, [{"id": payload.id, "text": payload.text, "source": payload.source, "embedding": vector}])
    return {"status": "upserted", "id": payload.id}


@app.post("/search")
def search(payload: SearchRequest) -> list[dict[str, Any]]:
    """语义搜索

    支持可选的 source 过滤，只搜索指定来源的文档。
    """
    vector = embed_svc.encode([payload.query])[0]
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
