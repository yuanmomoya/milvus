# image-search

CLIP 图片检索 Demo，支持文搜图和图搜图。先把图片放入 `sample_images/`，再调用 `/index/local` 入库。

```bash
cd milvus-master-course
./scripts/start.sh
cd demos/image-search
cp .env.example .env
mkdir -p sample_images
uvicorn app:app --reload --port 8002
```

```bash
curl -X POST http://localhost:8002/index/local
curl 'http://localhost:8002/search/text?q=red%20car&top_k=5'
curl -X POST http://localhost:8002/search/image -F 'file=@sample_images/example.jpg' -F 'top_k=5'
```
