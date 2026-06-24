"""共享文本向量化服务

封装 sentence-transformers 模型加载和编码逻辑，
多个 Demo 共享同一套向量化接口。
"""
from __future__ import annotations

from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """文本向量化服务，封装模型加载和编码逻辑"""

    def __init__(self, model_name: str) -> None:
        self.model = SentenceTransformer(model_name)
        dim = self.model.get_sentence_embedding_dimension()
        if dim is None:
            raise RuntimeError("无法读取 Embedding 模型维度")
        self.dim: int = dim

    def encode(self, texts: list[str]) -> list[list[float]]:
        """批量编码文本为向量

        normalize_embeddings=True 将向量归一化为单位向量，
        使得 COSINE 和 IP 度量等价，数值更稳定。
        """
        vectors = self.model.encode(
            texts, normalize_embeddings=True, show_progress_bar=False
        )
        return vectors.astype("float32").tolist()
