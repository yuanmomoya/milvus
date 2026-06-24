"""共享 Milvus 客户端工具

封装客户端创建和 HNSW 索引参数构建等通用操作。
"""
from __future__ import annotations

from pymilvus import MilvusClient


def build_milvus_client(uri: str, token: str) -> MilvusClient:
    """创建 Milvus 客户端连接，token 为空时表示本地未开启鉴权"""
    return MilvusClient(uri=uri, token=token or None)


def hnsw_index_params(
    field_name: str = "embedding",
    m: int = 16,
    ef_construction: int = 128,
) -> dict:
    """构建 HNSW + COSINE 索引参数（项目默认配置）

    返回可直接传入 index_params.add_index() 的关键字参数字典。
    """
    return {
        "field_name": field_name,
        "index_type": "HNSW",
        "metric_type": "COSINE",
        "params": {"M": m, "efConstruction": ef_construction},
    }
