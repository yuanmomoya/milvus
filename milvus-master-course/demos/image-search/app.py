"""图片检索 Demo - FastAPI 服务

使用 CLIP 模型实现文搜图和图搜图，向量存储在 Milvus 中。
对应教程第 30 章《图片检索系统》。

启动方式: uvicorn app:app --reload --port 8002
"""
from __future__ import annotations

import hashlib
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import torch
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse
from PIL import Image
from pymilvus import DataType, MilvusClient
from transformers import CLIPModel, CLIPProcessor

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)s %(name)s - %(message)s")
logger = logging.getLogger("image-search")


@dataclass(frozen=True)
class Settings:
    """配置项"""
    milvus_uri: str = os.getenv("MILVUS_URI", "http://localhost:19530")
    milvus_token: str = os.getenv("MILVUS_TOKEN", "")
    collection_name: str = os.getenv("COLLECTION_NAME", "course_image_vectors")
    clip_model: str = os.getenv("CLIP_MODEL", "openai/clip-vit-base-patch32")
    image_dir: Path = Path(os.getenv("IMAGE_DIR", "sample_images"))


settings = Settings()
app = FastAPI(title="Milvus Image Search", version="1.0.0")

# 加载 CLIP 模型（启动时一次性加载，避免每次请求重复加载）
processor = CLIPProcessor.from_pretrained(settings.clip_model)
model = CLIPModel.from_pretrained(settings.clip_model)
model.eval()  # 推理模式，关闭 dropout

# Milvus 客户端
client = MilvusClient(uri=settings.milvus_uri, token=settings.milvus_token or None)


def ensure_collection(dim: int = 512) -> None:
    """确保图片向量 Collection 存在"""
    if client.has_collection(settings.collection_name):
        client.load_collection(settings.collection_name)
        return
    schema = MilvusClient.create_schema(auto_id=False, enable_dynamic_field=False)
    schema.add_field("id", DataType.VARCHAR, is_primary=True, max_length=64)
    schema.add_field("image_path", DataType.VARCHAR, max_length=1024)
    schema.add_field("caption", DataType.VARCHAR, max_length=1024)
    schema.add_field("embedding", DataType.FLOAT_VECTOR, dim=dim)
    index_params = MilvusClient.prepare_index_params()
    index_params.add_index("embedding", index_type="HNSW", metric_type="COSINE", params={"M": 16, "efConstruction": 128})
    client.create_collection(settings.collection_name, schema=schema, index_params=index_params)
    client.load_collection(settings.collection_name)


def normalize(vector: torch.Tensor) -> list[float]:
    """L2 归一化向量，使 COSINE 和 IP 等价"""
    vector = vector / vector.norm(dim=-1, keepdim=True)
    return vector.detach().cpu().numpy().astype("float32")[0].tolist()


def embed_text(text: str) -> list[float]:
    """用 CLIP Text Encoder 编码文本查询"""
    inputs = processor(text=[text], return_tensors="pt", padding=True)
    with torch.no_grad():
        features = model.get_text_features(**inputs)
    return normalize(features)


def embed_image(image: Image.Image) -> list[float]:
    """用 CLIP Image Encoder 编码图片"""
    inputs = processor(images=image.convert("RGB"), return_tensors="pt")
    with torch.no_grad():
        features = model.get_image_features(**inputs)
    return normalize(features)


def search_vector(vector: list[float], top_k: int) -> list[dict[str, Any]]:
    """在 Milvus 中搜索最相似的图片"""
    ensure_collection()
    results = client.search(
        collection_name=settings.collection_name,
        data=[vector],
        anns_field="embedding",
        search_params={"metric_type": "COSINE", "params": {"ef": 64}},
        limit=top_k,
        output_fields=["image_path", "caption"],
    )
    return [{"score": float(hit.get("distance", 0.0)), **hit.get("entity", {})} for hit in results[0]]


@app.on_event("startup")
def startup() -> None:
    """应用启动时确保 Collection 就绪"""
    ensure_collection()


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    """简易 Web 界面"""
    return """
    <html><head><title>Milvus Image Search</title></head>
    <body style="font-family: sans-serif; max-width: 760px; margin: 40px auto;">
      <h1>Milvus 图片检索</h1>
      <h3>文搜图</h3>
      <form action="/search/text" method="get">
        <input name="q" placeholder="输入文本描述（英文效果更好）" style="width: 420px; padding: 8px;" />
        <input name="top_k" value="5" type="number" style="width: 80px; padding: 8px;" />
        <button type="submit">搜索</button>
      </form>
      <h3>图搜图</h3>
      <form action="/search/image" method="post" enctype="multipart/form-data">
        <input name="file" type="file" accept="image/*" />
        <input name="top_k" value="5" type="number" />
        <button type="submit">搜索</button>
      </form>
    </body></html>
    """


@app.post("/index/local")
def index_local_images() -> dict[str, int]:
    """批量导入本地图片目录到 Milvus

    遍历 IMAGE_DIR 下的图片文件，用 CLIP 编码后写入。
    生产环境应使用批量编码提高效率。
    """
    ensure_collection()
    rows: list[dict[str, Any]] = []
    for path in settings.image_dir.glob("*"):
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        try:
            image = Image.open(path)
            vector = embed_image(image)
            image_id = hashlib.sha1(str(path).encode("utf-8")).hexdigest()
            rows.append({"id": image_id, "image_path": str(path), "caption": path.stem, "embedding": vector})
        except Exception as e:
            logger.warning("跳过图片 %s: %s", path.name, e)
    if rows:
        client.upsert(settings.collection_name, rows)
    logger.info("导入 %d 张图片", len(rows))
    return {"indexed": len(rows)}


@app.get("/search/text")
def search_by_text(q: str, top_k: int = 5) -> list[dict[str, Any]]:
    """文搜图：用文本描述搜索相似图片

    CLIP 将文本和图片映射到同一向量空间，
    文本向量可以直接与图片向量比较相似度。
    """
    return search_vector(embed_text(q), top_k)


@app.post("/search/image")
def search_by_image(file: UploadFile = File(...), top_k: int = Form(5)) -> list[dict[str, Any]]:
    """图搜图：上传图片搜索相似图片"""
    image = Image.open(file.file)
    return search_vector(embed_image(image), top_k)
