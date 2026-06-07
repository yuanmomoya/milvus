# 33 FastAPI 接口开发

## 学习目标

学完本章后，你应该能够：

- 使用 FastAPI 封装 Milvus 搜索为 RESTful API。
- 设计向量搜索 API 的请求/响应模型。
- 实现健康检查、错误处理和请求验证。
- 管理 Milvus 客户端的生命周期。
- 部署生产级 FastAPI + Milvus 服务。

---

## 项目结构

```
fastapi-service/
├── app.py               # FastAPI 主入口
├── config.py            # 配置
├── models.py            # Pydantic 请求/响应模型
├── services/
│   ├── milvus_service.py    # Milvus 操作封装
│   └── embedding_service.py # Embedding 封装
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

---

## 配置管理

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Vector Search API"
    milvus_uri: str = "http://localhost:19530"
    milvus_token: str = ""
    collection_name: str = "documents"
    embedding_model: str = "BAAI/bge-small-zh-v1.5"
    default_top_k: int = 10
    max_top_k: int = 100
    log_level: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
```

---

## 请求/响应模型

```python
# models.py
from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000, description="搜索查询文本")
    top_k: int = Field(default=10, ge=1, le=100, description="返回结果数量")
    filter: str = Field(default="", description="Milvus 过滤表达式")
    output_fields: list[str] = Field(default_factory=lambda: ["text", "source"], description="返回字段")

class SearchHit(BaseModel):
    id: str
    score: float
    fields: dict

class SearchResponse(BaseModel):
    query: str
    results: list[SearchHit]
    total: int
    latency_ms: float

class UpsertRequest(BaseModel):
    documents: list[dict] = Field(..., min_length=1, max_length=1000)

class UpsertResponse(BaseModel):
    count: int
    message: str

class HealthResponse(BaseModel):
    status: str
    milvus: str
    collection: str
    version: str
```

---

## Milvus 服务层

```python
# services/milvus_service.py
import logging
from typing import Any
from pymilvus import MilvusClient
from pymilvus.exceptions import MilvusException

logger = logging.getLogger(__name__)

class MilvusService:
    def __init__(self, uri: str, token: str, collection: str):
        self._client = MilvusClient(uri=uri, token=token or None)
        self._collection = collection

    def health_check(self) -> bool:
        try:
            self._client.list_collections()
            return True
        except Exception:
            return False

    def search(
        self,
        vectors: list[list[float]],
        top_k: int = 10,
        filter_expr: str = "",
        output_fields: list[str] | None = None,
    ) -> list[list[dict[str, Any]]]:
        results = self._client.search(
            collection_name=self._collection,
            data=vectors,
            anns_field="embedding",
            search_params={"metric_type": "COSINE", "params": {"ef": 128}},
            limit=top_k,
            filter=filter_expr or None,
            output_fields=output_fields or ["text", "source"],
        )
        return [
            [
                {"id": hit["id"], "score": hit["distance"], "fields": hit["entity"]}
                for hit in hits
            ]
            for hits in results
        ]

    def upsert(self, data: list[dict]) -> int:
        result = self._client.upsert(collection_name=self._collection, data=data)
        return result["upsert_count"]

    def count(self) -> int:
        stats = self._client.get_collection_stats(self._collection)
        return stats["row_count"]
```

---

## FastAPI 主应用

```python
# app.py
import time
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from models import (
    SearchRequest, SearchResponse, SearchHit,
    UpsertRequest, UpsertResponse, HealthResponse,
)
from services.milvus_service import MilvusService
from services.embedding_service import EmbeddingService

logging.basicConfig(level=settings.log_level, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
logger = logging.getLogger("api")

# 全局服务实例
milvus_service: MilvusService | None = None
embedding_service: EmbeddingService | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时初始化，关闭时清理"""
    global milvus_service, embedding_service
    logger.info("初始化服务...")
    embedding_service = EmbeddingService(settings.embedding_model)
    milvus_service = MilvusService(settings.milvus_uri, settings.milvus_token, settings.collection_name)
    logger.info("服务就绪")
    yield
    logger.info("服务关闭")


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health():
    """健康检查"""
    milvus_ok = milvus_service.health_check() if milvus_service else False
    return HealthResponse(
        status="ok" if milvus_ok else "degraded",
        milvus="connected" if milvus_ok else "disconnected",
        collection=settings.collection_name,
        version="1.0.0",
    )


@app.post("/search", response_model=SearchResponse)
def search(req: SearchRequest):
    """向量搜索"""
    start = time.perf_counter()

    if not embedding_service or not milvus_service:
        raise HTTPException(status_code=503, detail="服务未就绪")

    # Embedding
    query_vector = embedding_service.encode([req.query])[0]

    # 搜索
    try:
        results = milvus_service.search(
            vectors=[query_vector],
            top_k=req.top_k,
            filter_expr=req.filter,
            output_fields=req.output_fields,
        )
    except Exception as e:
        logger.error("搜索失败: %s", e)
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

    hits = [SearchHit(**r) for r in results[0]]
    latency = (time.perf_counter() - start) * 1000

    return SearchResponse(
        query=req.query,
        results=hits,
        total=len(hits),
        latency_ms=round(latency, 2),
    )


@app.post("/upsert", response_model=UpsertResponse)
def upsert(req: UpsertRequest):
    """写入数据（需要包含 embedding 字段）"""
    if not milvus_service:
        raise HTTPException(status_code=503, detail="服务未就绪")

    try:
        count = milvus_service.upsert(req.documents)
    except Exception as e:
        logger.error("写入失败: %s", e)
        raise HTTPException(status_code=500, detail=f"写入失败: {str(e)}")

    return UpsertResponse(count=count, message="写入成功")


@app.post("/ingest")
def ingest(texts: list[str], source: str = "api"):
    """文本入库（自动 Embedding）"""
    if not embedding_service or not milvus_service:
        raise HTTPException(status_code=503, detail="服务未就绪")

    import hashlib
    vectors = embedding_service.encode(texts)
    data = [
        {
            "id": hashlib.sha256(f"{source}:{text[:50]}".encode()).hexdigest()[:32],
            "text": text,
            "source": source,
            "embedding": vec,
        }
        for text, vec in zip(texts, vectors)
    ]
    count = milvus_service.upsert(data)
    return {"count": count}
```

---

## 运行和测试

```bash
# 启动
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# 健康检查
curl http://localhost:8000/health

# 搜索
curl -X POST http://localhost:8000/search \
  -H 'Content-Type: application/json' \
  -d '{"query": "向量数据库的索引类型", "top_k": 5}'

# 入库
curl -X POST http://localhost:8000/ingest \
  -H 'Content-Type: application/json' \
  -d '["Milvus 支持 HNSW 索引", "IVF 是基于聚类的索引"]'

# 自动生成的 API 文档
# http://localhost:8000/docs（Swagger UI）
# http://localhost:8000/redoc（ReDoc）
```

---

## 生产部署

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

### docker-compose.yml

```yaml
services:
  api:
    build: .
    ports:
      - '8000:8000'
    environment:
      MILVUS_URI: http://milvus-standalone:19530
      EMBEDDING_MODEL: BAAI/bge-small-zh-v1.5
    depends_on:
      milvus-standalone:
        condition: service_healthy

  # Milvus 服务（引用项目根目录的配置）
  # ...
```

### Gunicorn + Uvicorn（多 Worker）

```bash
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

注意：多 Worker 时每个 Worker 都会加载 Embedding 模型，内存翻倍。如果模型大，建议用单 Worker + 异步，或把 Embedding 服务独立部署。

---

## 错误处理

```python
from fastapi import Request
from fastapi.responses import JSONResponse
from pymilvus.exceptions import MilvusException

@app.exception_handler(MilvusException)
async def milvus_exception_handler(request: Request, exc: MilvusException):
    logger.error("Milvus 错误: code=%s msg=%s", exc.code, exc.message)
    return JSONResponse(
        status_code=503,
        content={"detail": f"向量数据库错误: {exc.message}"},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error("未处理异常: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "内部服务错误"},
    )
```

---

## 常见错误

| 现象 | 原因 | 修复 |
|---|---|---|
| 启动时模型加载慢 | Embedding 模型首次下载 | 预下载模型或用 Docker 镜像内置 |
| 多 Worker 内存爆 | 每个 Worker 加载一份模型 | 减少 Worker 或独立 Embedding 服务 |
| CORS 报错 | 前端跨域请求被拒 | 添加 CORSMiddleware |
| 搜索超时 | Milvus 未 load 或网络问题 | 检查 Milvus 状态和连接 |
| 并发高时延迟飙升 | 单线程 Embedding 成为瓶颈 | 批量编码或 GPU 加速 |

---

## 面试题

1. **为什么用 lifespan 管理 Milvus 客户端而不是每次请求创建？**
   MilvusClient 内部维护连接池，创建开销大。lifespan 保证整个应用生命周期复用同一个客户端，避免连接泄漏和重复初始化。

2. **FastAPI 的异步和 pymilvus 的同步调用如何协调？**
   pymilvus 是同步库。在 FastAPI 中用同步路由函数（def 而非 async def），FastAPI 会自动在线程池中执行，不会阻塞事件循环。

3. **如何处理 Embedding 模型加载慢的问题？**
   在 lifespan 中预加载模型，启动时一次性完成。配合 Kubernetes 的 readinessProbe，模型加载完成前不接收流量。

4. **多 Worker 部署时 Milvus 连接如何管理？**
   每个 Worker 进程独立，各自创建 MilvusClient 实例。Milvus 服务端支持大量并发连接，通常不是瓶颈。

5. **如何限制 API 的请求频率？**
   使用 `slowapi` 或 `fastapi-limiter` 中间件。生产环境通常在 API Gateway（如 Nginx、Kong）层做限流。

---

## 练习题

1. **完整 API**：实现包含 health、search、upsert、delete 四个端点的完整 API。

2. **批量搜索**：添加 `/batch_search` 端点，支持一次请求多个查询。

3. **Docker 部署**：用 Dockerfile 打包服务，配合 docker-compose 一键启动 API + Milvus。

4. **压测**：用 `wrk` 或 `locust` 对 /search 端点压测，记录 QPS 和 P95 延迟。

---

## 小结

FastAPI + Milvus 是构建向量搜索 API 的标准组合。核心要点：lifespan 管理服务生命周期、Pydantic 模型做请求验证、分层架构（路由 → 服务 → 存储）保持代码清晰。生产部署注意 Embedding 模型的内存开销和多 Worker 策略。
