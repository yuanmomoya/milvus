# rag-system

生产化 RAG 教学 Demo：文本/PDF 入库、Chunk、Embedding、Milvus 召回、轻量 Rerank、Prompt、OpenAI Compatible API 回答和引用来源。

## 启动

```bash
cd milvus-master-course
./scripts/start.sh
cd demos/rag-system
cp .env.example .env
uvicorn main:app --reload --port 8001
```

## 导入文本

```bash
curl -X POST http://localhost:8001/ingest/text   -H 'Content-Type: application/json'   -d '{"source":"demo","text":"Milvus 支持高性能向量检索，常用于 RAG 知识库。"}'
```

## 提问

```bash
curl -X POST http://localhost:8001/ask   -H 'Content-Type: application/json'   -d '{"question":"Milvus 常用于什么场景？","top_k":5}'
```

## 导入 PDF

```bash
python ingest_pdf.py ./your_file.pdf
```
