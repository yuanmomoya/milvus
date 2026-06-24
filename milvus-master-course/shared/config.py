"""共享配置基类

提供 Milvus 连接和 Embedding 模型的通用配置字段，
各 Demo 继承后添加自己的专属配置。
"""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class BaseSettings:
    """Milvus 通用配置基类，所有字段均可通过环境变量覆盖"""

    milvus_uri: str = os.getenv("MILVUS_URI", "http://localhost:19530")
    milvus_token: str = os.getenv("MILVUS_TOKEN", "")
    collection_name: str = os.getenv("COLLECTION_NAME", "default_collection")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-zh-v1.5")
