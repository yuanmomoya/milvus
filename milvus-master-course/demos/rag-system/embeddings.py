"""RAG 知识库问答系统 - Embedding 服务封装

复用 shared.text_embedding.EmbeddingService，
保持 RAG 系统内部接口稳定。
"""
from __future__ import annotations

import sys
from pathlib import Path

# 将 milvus-master-course/ 加入搜索路径，以便导入 shared 包
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from shared.text_embedding import EmbeddingService

__all__ = ["EmbeddingService"]
