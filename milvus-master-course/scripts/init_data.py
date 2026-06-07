"""初始化样例数据脚本

创建 Collection 并写入示例文档，验证 Milvus 连接和基本搜索功能。
等同于 demos/basic-search/main.py，放在 scripts/ 下方便全局调用。
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv
from pymilvus import DataType, MilvusClient
from sentence_transformers import SentenceTransformer

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger("init-data")


@dataclass(frozen=True)
class Settings:
    """配置项，通过环境变量或 .env 文件覆盖"""
    milvus_uri: str = os.getenv("MILVUS_URI", "http://localhost:19530")
    milvus_token: str = os.getenv("MILVUS_TOKEN", "")
    collection_name: str = os.getenv("COLLECTION_NAME", "course_basic_docs")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-zh-v1.5")
    recreate: bool = os.getenv("RECREATE_COLLECTION", "false").lower() == "true"
    top_k: int = int(os.getenv("TOP_K", "3"))
    ef_search: int = int(os.getenv("EF_SEARCH", "64"))


def build_client(settings: Settings) -> MilvusClient:
    """创建 Milvus 客户端"""
    token = settings.milvus_token or None
    return MilvusClient(uri=settings.milvus_uri, token=token)


def ensure_collection(client: MilvusClient, name: str, dim: int, recreate: bool) -> None:
    """确保 Collection 存在且已加载"""
    if recreate and client.has_collection(name):
        logger.info("删除旧 Collection: %s", name)
        client.drop_collection(name)

    if client.has_collection(name):
        logger.info("Collection 已存在: %s", name)
        client.load_collection(name)
        return

    # 定义 Schema
    schema = MilvusClient.create_schema(auto_id=False, enable_dynamic_field=False)
    schema.add_field(field_name="id", datatype=DataType.VARCHAR, is_primary=True, max_length=64)
    schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=2048)
    schema.add_field(field_name="source", datatype=DataType.VARCHAR, max_length=256)
    schema.add_field(field_name="embedding", datatype=DataType.FLOAT_VECTOR, dim=dim)

    # HNSW 索引 + COSINE 度量
    index_params = MilvusClient.prepare_index_params()
    index_params.add_index(
        field_name="embedding",
        index_name="embedding_hnsw",
        index_type="HNSW",
        metric_type="COSINE",
        params={"M": 16, "efConstruction": 128},
    )

    logger.info("创建 Collection: %s dim=%s", name, dim)
    client.create_collection(collection_name=name, schema=schema, index_params=index_params)
    client.load_collection(name)


def embed_texts(model: SentenceTransformer, texts: list[str]) -> list[list[float]]:
    """批量文本向量化"""
    vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return vectors.astype("float32").tolist()


def seed_documents(client: MilvusClient, settings: Settings, model: SentenceTransformer) -> None:
    """写入示例文档数据"""
    docs = [
        {"id": "doc-001", "text": "Milvus 是面向 AI 应用的高性能向量数据库。", "source": "intro"},
        {"id": "doc-002", "text": "HNSW 是一种基于图的近似最近邻搜索索引。", "source": "index"},
        {"id": "doc-003", "text": "RAG 系统通常包含文档切块、向量召回、重排序和大模型生成。", "source": "rag"},
        {"id": "doc-004", "text": "CLIP 可以把图片和文本映射到同一个多模态向量空间。", "source": "multimodal"},
        {"id": "doc-005", "text": "生产环境需要关注 Milvus 的 Segment、Compaction、监控和容量规划。", "source": "ops"},
    ]
    vectors = embed_texts(model, [doc["text"] for doc in docs])
    rows: list[dict[str, Any]] = []
    for doc, vector in zip(docs, vectors, strict=True):
        rows.append({**doc, "embedding": vector})

    logger.info("写入/更新样例数据: %s 条", len(rows))
    client.upsert(collection_name=settings.collection_name, data=rows)


def search(client: MilvusClient, settings: Settings, model: SentenceTransformer, query: str) -> None:
    """执行语义搜索并打印结果"""
    query_vector = embed_texts(model, [query])[0]
    results = client.search(
        collection_name=settings.collection_name,
        data=[query_vector],
        anns_field="embedding",
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
    model = SentenceTransformer(settings.embedding_model)
    dim = model.get_sentence_embedding_dimension()
    if dim is None:
        raise RuntimeError("无法读取模型向量维度")

    client = build_client(settings)
    ensure_collection(client, settings.collection_name, dim, settings.recreate)
    seed_documents(client, settings, model)
    search(client, settings, model, "如何构建一个 RAG 知识库？")


if __name__ == "__main__":
    main()
