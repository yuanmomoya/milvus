"""共享 CLIP 多模态向量化服务

封装 CLIP 模型加载、文本编码和图片编码逻辑，
image-search 和 multimodal-search Demo 共享同一套接口。
"""
from __future__ import annotations

import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor


class CLIPEmbeddingService:
    """CLIP 多模态向量化服务"""

    def __init__(self, model_name: str) -> None:
        self.processor = CLIPProcessor.from_pretrained(model_name)
        self.model = CLIPModel.from_pretrained(model_name)
        self.model.eval()

    @staticmethod
    def _normalize(vector: torch.Tensor) -> list[float]:
        """L2 归一化向量，使 COSINE 和 IP 等价"""
        vector = vector / vector.norm(dim=-1, keepdim=True)
        return vector.detach().cpu().numpy().astype("float32")[0].tolist()

    def encode_text(self, text: str) -> list[float]:
        """用 CLIP Text Encoder 编码文本查询"""
        inputs = self.processor(text=[text], return_tensors="pt", padding=True)
        with torch.no_grad():
            features = self.model.get_text_features(**inputs)
        return self._normalize(features)

    def encode_image(self, image: Image.Image) -> list[float]:
        """用 CLIP Image Encoder 编码图片"""
        inputs = self.processor(images=image.convert("RGB"), return_tensors="pt")
        with torch.no_grad():
            features = self.model.get_image_features(**inputs)
        return self._normalize(features)
