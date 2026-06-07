# basic-search

文本向量检索最小可运行 Demo：创建 Collection、写入中文样例、HNSW 检索 TopK。

## 启动

```bash
cd milvus-master-course
./scripts/start.sh
cd demos/basic-search
cp .env.example .env
python main.py
```

## Docker 运行

```bash
docker compose run --rm demo
```

## curl 示例

本 Demo 是 CLI。如果要通过 HTTP 调用，请看 `../fastapi-service`。
