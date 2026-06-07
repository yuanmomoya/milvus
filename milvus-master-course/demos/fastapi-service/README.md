# fastapi-service

Milvus 检索服务 API Demo。

```bash
cd milvus-master-course
./scripts/start.sh
cd demos/fastapi-service
cp .env.example .env
uvicorn app:app --reload --port 8000
```

```bash
curl -X POST http://localhost:8000/documents   -H 'Content-Type: application/json'   -d '{"id":"1","text":"Milvus 可以用于语义搜索和 RAG。","source":"demo"}'

curl -X POST http://localhost:8000/search   -H 'Content-Type: application/json'   -d '{"query":"向量数据库能做什么？","top_k":5}'
```
