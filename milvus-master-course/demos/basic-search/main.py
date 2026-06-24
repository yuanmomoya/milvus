"""基础语义搜索 Demo

演示 Milvus 的最小闭环：连接 → 创建 Collection → 生成向量 → 写入 → 搜索。
对应教程第 03 章《Milvus 快速开始》。
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pymilvus import DataType, MilvusClient

# 将 milvus-master-course/ 加入搜索路径，以便导入 shared 包
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from shared.config import BaseSettings
from shared.logging_setup import configure_logging
from shared.milvus_client import build_milvus_client, hnsw_index_params
from shared.text_embedding import EmbeddingService

logger = configure_logging("basic-search")


@dataclass(frozen=True)
class Settings(BaseSettings):
    """从环境变量读取配置，支持 .env 文件覆盖"""
    collection_name: str = os.getenv("COLLECTION_NAME", "course_basic_docs")
    recreate: bool = os.getenv("RECREATE_COLLECTION", "false").lower() == "true"
    top_k: int = int(os.getenv("TOP_K", "3"))
    ef_search: int = int(os.getenv("EF_SEARCH", "64"))


def ensure_collection(client: MilvusClient, name: str, dim: int, recreate: bool) -> None:
    """确保 Collection 存在且已加载，幂等操作"""
    if recreate and client.has_collection(name):
        logger.info("删除旧 Collection: %s", name)
        client.drop_collection(name)

    if client.has_collection(name):
        logger.info("Collection 已存在: %s", name)
        client.load_collection(name)
        return

    # 定义 Schema：主键 + 文本 + 来源 + 向量
    schema = MilvusClient.create_schema(auto_id=False, enable_dynamic_field=False)
    schema.add_field(field_name="id", datatype=DataType.VARCHAR, is_primary=True, max_length=64)
    schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=2048)
    schema.add_field(field_name="source", datatype=DataType.VARCHAR, max_length=256)
    schema.add_field(field_name="embedding", datatype=DataType.FLOAT_VECTOR, dim=dim)

    # 创建 HNSW 索引，COSINE 度量适合归一化后的文本向量
    index_params = MilvusClient.prepare_index_params()
    index_params.add_index(**hnsw_index_params())

    logger.info("创建 Collection: %s dim=%s", name, dim)
    client.create_collection(collection_name=name, schema=schema, index_params=index_params)
    # 搜索前必须 load，将数据加载到 QueryNode 内存
    client.load_collection(name)


def seed_documents(client: MilvusClient, settings: Settings, embed_svc: EmbeddingService) -> None:
    """写入示例文档，使用 upsert 保证幂等（重复运行不会产生重复数据）"""
    docs = [
        {"id": "doc-001", "text": "Milvus 是面向 AI 应用的高性能向量数据库。", "source": "intro"},
        {"id": "doc-002", "text": "HNSW 是一种基于图的近似最近邻搜索索引。", "source": "index"},
        {"id": "doc-003", "text": "RAG 系统通常包含文档切块、向量召回、重排序和大模型生成。", "source": "rag"},
        {"id": "doc-004", "text": "CLIP 可以把图片和文本映射到同一个多模态向量空间。", "source": "multimodal"},
        {"id": "doc-005", "text": "生产环境需要关注 Milvus 的 Segment、Compaction、监控和容量规划。", "source": "ops"},
    ]
    vectors = embed_svc.encode([doc["text"] for doc in docs])
    rows: list[dict[str, Any]] = []
    for doc, vector in zip(docs, vectors, strict=True):
        rows.append({**doc, "embedding": vector})

    logger.info("写入/更新样例数据: %s 条", len(rows))
    client.upsert(collection_name=settings.collection_name, data=rows)


def search(client: MilvusClient, settings: Settings, embed_svc: EmbeddingService, query: str) -> None:
    """执行语义搜索并打印结果"""
    query_vector = embed_svc.encode([query])[0]
    results = client.search(
        collection_name=settings.collection_name,
        data=[query_vector],
        anns_field="embedding",
        # ef 控制 HNSW 搜索时的候选集大小，越大召回越高但延迟也越高
        search_params={"metric_type": "COSINE", "params": {"ef": settings.ef_search}},
        limit=settings.top_k,
        output_fields=["text", "source"],
    )

    print(f"\n查询：{query}")
    for rank, hit in enumerate(results[0], start=1):
        entity = hit.get("entity", {})
        print(f"{rank}. score={hit.get('distance'):.4f} source={entity.get('source')} text={entity.get('text')}")


def main() -> None:
    settings = Settings()
    logger.info("加载 Embedding 模型: %s", settings.embedding_model)
    embed_svc = EmbeddingService(settings.embedding_model)

    client = build_milvus_client(settings.milvus_uri, settings.milvus_token)
    ensure_collection(client, settings.collection_name, embed_svc.dim, settings.recreate)
    seed_documents(client, settings, embed_svc)
    search(client, settings, embed_svc, "如何构建一个 RAG 知识库？")


if __name__ == "__main__":
    main()
