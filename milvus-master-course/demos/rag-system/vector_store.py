"""RAG 知识库问答系统 - Milvus 向量存储层

封装 Collection 创建、数据写入和向量搜索逻辑。
对应教程第 23 章《RAG 知识库实战》。
"""
from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from typing import Any

from pymilvus import DataType, MilvusClient

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Chunk:
    """文档切块数据结构"""
    text: str       # 切块文本内容
    source: str     # 来源文件名
    page: int = 0   # 所在页码
    chunk_id: int = 0  # 块序号


def stable_id(source: str, page: int, chunk_id: int, text: str) -> str:
    """生成稳定的主键：相同内容多次入库不会产生重复数据"""
    raw = f"{source}:{page}:{chunk_id}:{text}".encode("utf-8")
    return hashlib.sha1(raw).hexdigest()


class RagVectorStore:
    """RAG 向量存储：管理 Collection 生命周期和 CRUD 操作"""

    def __init__(self, uri: str, token: str, collection_name: str, dim: int) -> None:
        self.collection_name = collection_name
        self.client = MilvusClient(uri=uri, token=token or None)
        self.dim = dim
        self.ensure_collection()

    def ensure_collection(self) -> None:
        """确保 Collection 存在且已加载（幂等操作）"""
        if self.client.has_collection(self.collection_name):
            self.client.load_collection(self.collection_name)
            return

        # Schema 设计：主键 + 文本 + 追溯字段 + 向量
        schema = MilvusClient.create_schema(auto_id=False, enable_dynamic_field=False)
        schema.add_field("id", DataType.VARCHAR, is_primary=True, max_length=64)
        schema.add_field("text", DataType.VARCHAR, max_length=8192)
        schema.add_field("source", DataType.VARCHAR, max_length=512)
        schema.add_field("page", DataType.INT64)
        schema.add_field("chunk_id", DataType.INT64)
        schema.add_field("embedding", DataType.FLOAT_VECTOR, dim=self.dim)

        # HNSW 索引：中小规模文本检索的默认选择
        index_params = MilvusClient.prepare_index_params()
        index_params.add_index(
            "embedding",
            index_type="HNSW",
            metric_type="COSINE",
            params={"M": 16, "efConstruction": 128},
        )
        self.client.create_collection(self.collection_name, schema=schema, index_params=index_params)
        self.client.load_collection(self.collection_name)
        logger.info("RAG Collection 创建完成: %s", self.collection_name)

    def upsert_chunks(self, chunks: list[Chunk], vectors: list[list[float]]) -> int:
        """批量写入切块数据，使用 upsert 保证幂等"""
        rows: list[dict[str, Any]] = []
        for chunk, vector in zip(chunks, vectors, strict=True):
            rows.append(
                {
                    "id": stable_id(chunk.source, chunk.page, chunk.chunk_id, chunk.text),
                    "text": chunk.text,
                    "source": chunk.source,
                    "page": chunk.page,
                    "chunk_id": chunk.chunk_id,
                    "embedding": vector,
                }
            )
        if not rows:
            return 0
        self.client.upsert(self.collection_name, rows)
        return len(rows)

    def search(self, vector: list[float], top_k: int) -> list[dict[str, Any]]:
        """向量相似度搜索，返回 TopK 最相关的切块"""
        results = self.client.search(
            collection_name=self.collection_name,
            data=[vector],
            anns_field="embedding",
            # ef=96 在召回率和延迟之间取平衡
            search_params={"metric_type": "COSINE", "params": {"ef": 96}},
            limit=top_k,
            output_fields=["text", "source", "page", "chunk_id"],
        )
        hits: list[dict[str, Any]] = []
        for hit in results[0]:
            entity = hit.get("entity", {})
            hits.append({"score": float(hit.get("distance", 0.0)), **entity})
        return hits
