"""RAG 知识库问答系统 - Embedding 服务封装

封装 sentence-transformers 模型，提供统一的编码接口。
生产环境可替换为 OpenAI API 或独立的 Embedding 微服务。
"""
from __future__ import annotations

from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """文本向量化服务，封装模型加载和编码逻辑"""

    def __init__(self, model_name: str) -> None:
        # 加载模型（首次运行会从 HuggingFace 下载）
        self.model = SentenceTransformer(model_name)
        dim = self.model.get_sentence_embedding_dimension()
        if dim is None:
            raise RuntimeError("无法读取 Embedding 模型维度")
        self.dim = dim

    def encode(self, texts: list[str]) -> list[list[float]]:
        """批量编码文本为向量

        normalize_embeddings=True 将向量归一化为单位向量，
        使得 COSINE 和 IP 度量等价，数值更稳定。
        """
        vectors = self.model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        return vectors.astype("float32").tolist()
