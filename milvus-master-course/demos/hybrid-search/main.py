"""混合检索 Demo（多向量字段 + RRF 融合）

演示在同一个 Collection 中使用多个向量字段（标题向量 + 正文向量），
通过 hybrid_search + RRF 融合排序获得更好的检索效果。
对应教程第 13 章《混合检索 HybridSearch》。
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pymilvus import AnnSearchRequest, DataType, MilvusClient, RRFRanker

# 将 milvus-master-course/ 加入搜索路径，以便导入 shared 包
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from shared.config import BaseSettings
from shared.logging_setup import configure_logging
from shared.milvus_client import build_milvus_client, hnsw_index_params
from shared.text_embedding import EmbeddingService

logger = configure_logging("hybrid-search")


@dataclass(frozen=True)
class Settings(BaseSettings):
    """配置项"""
    collection_name: str = os.getenv("COLLECTION_NAME", "course_hybrid_docs")
    recreate: bool = os.getenv("RECREATE_COLLECTION", "false").lower() == "true"
    top_k: int = int(os.getenv("TOP_K", "5"))


def ensure_collection(client: MilvusClient, settings: Settings, dim: int) -> None:
    """创建包含两个向量字段的 Collection（标题向量 + 正文向量）"""
    if settings.recreate and client.has_collection(settings.collection_name):
        client.drop_collection(settings.collection_name)
    if client.has_collection(settings.collection_name):
        client.load_collection(settings.collection_name)
        return

    schema = MilvusClient.create_schema(auto_id=False, enable_dynamic_field=False)
    schema.add_field("id", DataType.VARCHAR, is_primary=True, max_length=64)
    schema.add_field("title", DataType.VARCHAR, max_length=256)
    schema.add_field("body", DataType.VARCHAR, max_length=2048)
    schema.add_field("category", DataType.VARCHAR, max_length=64)
    # 两个向量字段：分别对标题和正文编码
    schema.add_field("title_vector", DataType.FLOAT_VECTOR, dim=dim)
    schema.add_field("body_vector", DataType.FLOAT_VECTOR, dim=dim)

    # 每个向量字段独立建索引
    index_params = MilvusClient.prepare_index_params()
    for field in ["title_vector", "body_vector"]:
        index_params.add_index(**hnsw_index_params(field_name=field))

    client.create_collection(settings.collection_name, schema=schema, index_params=index_params)
    client.load_collection(settings.collection_name)


def seed(client: MilvusClient, settings: Settings, embed_svc: EmbeddingService) -> None:
    """写入示例数据：标题和正文分别编码为向量"""
    docs = [
        {"id": "hy-001", "title": "Milvus 架构", "body": "Proxy、QueryNode、DataNode 和 Coord 共同完成写入和查询。", "category": "milvus"},
        {"id": "hy-002", "title": "HNSW 调优", "body": "ef 越大召回通常越高，但延迟也会上升。", "category": "index"},
        {"id": "hy-003", "title": "RAG 召回优化", "body": "可以结合向量召回、关键词召回、Rerank 和 Query Rewrite。", "category": "rag"},
        {"id": "hy-004", "title": "图片检索", "body": "CLIP 支持文搜图和图搜图，适合多模态搜索。", "category": "image"},
    ]
    title_vectors = embed_svc.encode([doc["title"] for doc in docs])
    body_vectors = embed_svc.encode([doc["body"] for doc in docs])
    rows: list[dict[str, Any]] = []
    for doc, title_vector, body_vector in zip(docs, title_vectors, body_vectors, strict=True):
        rows.append({**doc, "title_vector": title_vector, "body_vector": body_vector})
    client.upsert(settings.collection_name, rows)


def hybrid_search(client: MilvusClient, settings: Settings, embed_svc: EmbeddingService, query: str) -> None:
    """混合搜索：同时搜索标题和正文向量，用 RRF 融合排序

    RRF（Reciprocal Rank Fusion）只看排名不看分数绝对值，
    适合融合不同向量字段的搜索结果。
    """
    qv = embed_svc.encode([query])[0]

    # 标题向量搜索请求
    title_req = AnnSearchRequest(
        data=[qv],
        anns_field="title_vector",
        param={"metric_type": "COSINE", "params": {"ef": 64}},
        limit=settings.top_k,
    )
    # 正文向量搜索请求
    body_req = AnnSearchRequest(
        data=[qv],
        anns_field="body_vector",
        param={"metric_type": "COSINE", "params": {"ef": 64}},
        limit=settings.top_k,
    )

    # 执行混合搜索，RRF k=60 是常用默认值
    results = client.hybrid_search(
        collection_name=settings.collection_name,
        reqs=[title_req, body_req],
        ranker=RRFRanker(k=60),
        limit=settings.top_k,
        output_fields=["title", "body", "category"],
    )

    print(f"\nHybrid 查询：{query}")
    for rank, hit in enumerate(results[0], start=1):
        entity = hit.get("entity", {})
        print(f"{rank}. score={hit.get('distance'):.4f} [{entity.get('category')}] {entity.get('title')} - {entity.get('body')}")


def main() -> None:
    settings = Settings()
    embed_svc = EmbeddingService(settings.embedding_model)
    client = build_milvus_client(settings.milvus_uri, settings.milvus_token)
    ensure_collection(client, settings, embed_svc.dim)
    seed(client, settings, embed_svc)
    hybrid_search(client, settings, embed_svc, "怎样提升 RAG 的召回效果？")


if __name__ == "__main__":
    main()
