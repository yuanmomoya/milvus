"""多模态检索 Demo - FastAPI 服务

在同一个 Collection 中混合存储图片和文本向量（CLIP 共享空间），
支持文搜图、图搜图和全模态搜索。
对应教程第 31 章《CLIP 多模态检索》。

启动方式: uvicorn app:app --reload --port 8003
"""
from __future__ import annotations

import hashlib
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse
from PIL import Image
from pymilvus import DataType, MilvusClient

# 将 milvus-master-course/ 加入搜索路径，以便导入 shared 包
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from shared.clip_embedding import CLIPEmbeddingService
from shared.config import BaseSettings
from shared.logging_setup import configure_logging
from shared.milvus_client import build_milvus_client, hnsw_index_params

logger = configure_logging("multimodal-search")


@dataclass(frozen=True)
class Settings(BaseSettings):
    """配置项"""
    collection_name: str = os.getenv("COLLECTION_NAME", "course_multimodal_vectors")
    clip_model: str = os.getenv("CLIP_MODEL", "openai/clip-vit-base-patch32")
    image_dir: Path = Path(os.getenv("IMAGE_DIR", "sample_images"))


settings = Settings()
app = FastAPI(title="Milvus Multimodal Search", version="1.0.0")

# 加载 CLIP 模型（图片和文本共享同一个向量空间）
clip_svc = CLIPEmbeddingService(settings.clip_model)

client = build_milvus_client(settings.milvus_uri, settings.milvus_token)


def ensure_collection(dim: int = 512) -> None:
    """确保多模态 Collection 存在

    与单模态图片检索的区别：这里图片和文本的向量存在同一个字段中，
    因为 CLIP 保证它们在同一个向量空间。
    """
    if client.has_collection(settings.collection_name):
        client.load_collection(settings.collection_name)
        return
    schema = MilvusClient.create_schema(auto_id=False, enable_dynamic_field=False)
    schema.add_field("id", DataType.VARCHAR, is_primary=True, max_length=64)
    schema.add_field("image_path", DataType.VARCHAR, max_length=1024)
    schema.add_field("caption", DataType.VARCHAR, max_length=1024)
    schema.add_field("embedding", DataType.FLOAT_VECTOR, dim=dim)
    index_params = MilvusClient.prepare_index_params()
    index_params.add_index(**hnsw_index_params())
    client.create_collection(settings.collection_name, schema=schema, index_params=index_params)
    client.load_collection(settings.collection_name)


def search_vector(vector: list[float], top_k: int) -> list[dict[str, Any]]:
    """向量搜索（不区分模态，因为共享同一向量空间）"""
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
    ensure_collection()


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    """Web 界面"""
    return """
    <html><head><title>Milvus Multimodal Search</title></head>
    <body style="font-family: sans-serif; max-width: 760px; margin: 40px auto;">
      <h1>Milvus 多模态检索</h1>
      <p>图片和文本在同一个 CLIP 向量空间中，支持跨模态搜索。</p>
      <h3>文搜图</h3>
      <form action="/search/text" method="get">
        <input name="q" placeholder="输入文本描述" style="width: 420px; padding: 8px;" />
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
    """批量导入本地图片"""
    ensure_collection()
    rows: list[dict[str, Any]] = []
    for path in settings.image_dir.glob("*"):
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        try:
            image = Image.open(path)
            vector = clip_svc.encode_image(image)
            image_id = hashlib.sha1(str(path).encode("utf-8")).hexdigest()
            rows.append({"id": image_id, "image_path": str(path), "caption": path.stem, "embedding": vector})
        except Exception as e:
            logger.warning("跳过 %s: %s", path.name, e)
    if rows:
        client.upsert(settings.collection_name, rows)
    return {"indexed": len(rows)}


@app.get("/search/text")
def search_by_text(q: str, top_k: int = 5) -> list[dict[str, Any]]:
    """文搜图：CLIP 文本向量搜索图片向量"""
    return search_vector(clip_svc.encode_text(q), top_k)


@app.post("/search/image")
def search_by_image(file: UploadFile = File(...), top_k: int = Form(5)) -> list[dict[str, Any]]:
    """图搜图：CLIP 图片向量搜索相似图片"""
    image = Image.open(file.file)
    return search_vector(clip_svc.encode_image(image), top_k)
