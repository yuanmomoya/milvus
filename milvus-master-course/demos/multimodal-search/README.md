# multimodal-search

多模态检索 Demo：用 CLIP 将文本和图片映射到同一向量空间，支持文搜图、图搜图。

```bash
cd milvus-master-course/demos/multimodal-search
cp .env.example .env
mkdir -p sample_images
uvicorn app:app --reload --port 8003
```
