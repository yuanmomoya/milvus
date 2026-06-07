# Milvus 从入门到精通

这是一套面向 Python 开发者、AI 应用开发者、RAG 工程师和后端工程师的 Milvus 系统教程。项目按“教程文档 + 可运行 Demo + 部署脚本 + 生产实践”的方式组织，目标不是背 API，而是理解向量数据库为什么这样设计，以及如何把 Milvus 用进真实业务。

## 版本基线

| 组件 | 版本 |
|---|---:|
| Milvus | 2.6.15 |
| pymilvus | 2.6.12 |
| Python | 3.11 |
| 部署方式 | Docker Compose 单机，生产章节扩展到集群 |
| Embedding | sentence-transformers / CLIP |
| 服务框架 | FastAPI |
| RAG 编排 | LangChain，OpenAI Compatible API |

说明：Milvus 3.0-beta 只在第 40 章作为趋势和迁移观察提及，主线教程全部按当前稳定 2.6.x 编写。

参考来源：

- [Milvus Docker Compose 配置文档](https://milvus.io/docs/configure-docker.md)
- [Milvus Python SDK 安装文档](https://milvus.io/docs/install-pymilvus.md/)
- [PyMilvus 发布记录](https://github.com/milvus-io/pymilvus/releases)

## 学习路径

```mermaid
flowchart LR
    A[向量数据库基础] --> B[Milvus 架构与部署]
    B --> C[pymilvus 开发]
    C --> D[索引与查询优化]
    D --> E[RAG 系统]
    E --> F[多模态检索]
    F --> G[生产部署与压测]
    G --> H[源码与面试]
```

建议学习顺序：

1. `01-09`：建立向量数据库和 Milvus 基础。
2. `10-17`：掌握索引、过滤、分区、批量写入和查询调优。
3. `18-21`：理解生产部署、高可用、监控和最佳实践。
4. `22-29`：构建 RAG 知识库，接入 LangChain / LlamaIndex。
5. `30-34`：实现图片、多模态和完整 AI 搜索服务。
6. `35-40`：面向海量数据、Benchmark、Debug、源码和趋势。

## 项目结构

```text
milvus-master-course/
├── README.md
├── requirements.txt
├── docker-compose.yml
├── .env.example
├── .gitignore
├── configs/
│   └── milvus.yaml
├── docs/
│   ├── 00-教程规划与学习路径.md
│   └── 01-向量数据库基础.md ... 40-未来趋势与生态.md
├── demos/
│   ├── basic-search/
│   ├── hybrid-search/
│   ├── rag-system/
│   ├── image-search/
│   ├── multimodal-search/
│   ├── fastapi-service/
│   └── benchmark/
└── scripts/
    ├── start.sh
    ├── stop.sh
    ├── init_data.py
    └── benchmark.py
```

## 快速开始

```bash
cd milvus-master-course
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
./scripts/start.sh
python scripts/init_data.py
```

Windows PowerShell：

```powershell
cd milvus-master-course
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
docker compose up -d
python scripts/init_data.py
```

## 章节总览

| 序号 | 章节 | 核心知识点 |
|---:|---|---|
| 01 | [向量数据库基础](docs/01-向量数据库基础.md) | 向量、Embedding、相似度度量、暴力检索与 ANN 的复杂度差异、HNSW、IVF、PQ 的直观模型 |
| 02 | [Milvus整体架构](docs/02-Milvus整体架构.md) | Proxy、RootCoord、DataCoord、QueryCoord、IndexCoord、DataNode、QueryNode、IndexNode 的职责边界、etcd、MinIO、Pulsar 在集群中的作用 |
| 03 | [Milvus快速开始](docs/03-Milvus快速开始.md) | 本地启动 Milvus、安装 Python 3.11 依赖、创建 Collection 并写入样例数据 |
| 04 | [Docker部署Milvus](docs/04-Docker部署Milvus.md) | Docker Compose 服务组成、端口、卷、健康检查、Linux/macOS/Windows 启动差异 |
| 05 | [pymilvus完全指南](docs/05-pymilvus完全指南.md) | MilvusClient 连接方式、Schema、Index、Load、Insert、Search、过滤表达式 |
| 06 | [Collection设计](docs/06-Collection设计.md) | 主键设计、向量字段与标量字段、动态字段取舍 |
| 07 | [向量数据建模](docs/07-向量数据建模.md) | 文本、图片、多模态数据建模、元数据字段、多租户字段 |
| 08 | [Embedding模型详解](docs/08-Embedding模型详解.md) | Embedding 模型选择、归一化与度量匹配、中文模型实践 |
| 09 | [向量索引原理](docs/09-向量索引原理.md) | FLAT、IVF、HNSW、PQ 家族、索引构建流程、索引参数与召回率 |
| 10 | [IVF原理与实战](docs/10-IVF原理与实战.md) | KMeans 聚类中心、nlist 与 nprobe、Recall 和 Latency 的平衡 |
| 11 | [HNSW原理与实战](docs/11-HNSW原理与实战.md) | 小世界图、M、efConstruction、ef、插入与搜索路径 |
| 12 | [PQ与量化压缩](docs/12-PQ与量化压缩.md) | Product Quantization、码本训练、压缩率 |
| 13 | [混合检索HybridSearch](docs/13-混合检索HybridSearch.md) | 稠密召回与关键词召回、多向量字段、RRFRanker 与加权融合 |
| 14 | [标量过滤ScalarFilter](docs/14-标量过滤ScalarFilter.md) | 表达式过滤、倒排/标量索引、过滤前置与后置 |
| 15 | [分区Partition设计](docs/15-分区Partition设计.md) | Partition Key、按租户分区、按时间分区 |
| 16 | [批量写入优化](docs/16-批量写入优化.md) | 批大小、并发写入、Flush 策略 |
| 17 | [查询性能调优](docs/17-查询性能调优.md) | TopK、ef、nprobe、查询并发、缓存和预热 |
| 18 | [Milvus集群部署](docs/18-Milvus集群部署.md) | 集群模式组件、Helm 部署、存储依赖 |
| 19 | [Milvus高可用设计](docs/19-Milvus高可用设计.md) | 副本、故障域、对象存储可靠性 |
| 20 | [Milvus监控体系](docs/20-Milvus监控体系.md) | 指标体系、Prometheus、Grafana |
| 21 | [Milvus生产最佳实践](docs/21-Milvus生产最佳实践.md) | 容量规划、配置基线、发布变更 |
| 22 | [RAG架构基础](docs/22-RAG架构基础.md) | RAG 基本链路、Chunk 策略、Embedding 入库 |
| 23 | [RAG知识库实战](docs/23-RAG知识库实战.md) | PDF 解析、文档切块、向量入库 |
| 24 | [RAG召回优化](docs/24-RAG召回优化.md) | Query Rewrite、多查询扩展、TopK 选择 |
| 25 | [Rerank重排序](docs/25-Rerank重排序.md) | Cross-Encoder、BGE Reranker、融合排序 |
| 26 | [多路召回架构](docs/26-多路召回架构.md) | BM25、Dense、Sparse、RRF、加权融合 |
| 27 | [Agent结合Milvus](docs/27-Agent结合Milvus.md) | Agent 记忆、工具调用、向量检索工具 |
| 28 | [LangChain集成](docs/28-LangChain集成.md) | LangChain VectorStore、Retriever、Runnable |
| 29 | [LlamaIndex集成](docs/29-LlamaIndex集成.md) | LlamaIndex Index、Node Parser、Retriever |
| 30 | [图片检索系统](docs/30-图片检索系统.md) | 图片 Embedding、CLIP 图搜图、TopK |
| 31 | [CLIP多模态检索](docs/31-CLIP多模态检索.md) | 文搜图、图搜图、同一向量空间 |
| 32 | [视频检索思路](docs/32-视频检索思路.md) | 抽帧、镜头切分、关键帧索引 |
| 33 | [FastAPI接口开发](docs/33-FastAPI接口开发.md) | 服务分层、Pydantic 入参、错误码 |
| 34 | [构建完整AI搜索系统](docs/34-构建完整AI搜索系统.md) | 整体 AI 搜索架构、检索服务、RAG 服务 |
| 35 | [海量数据架构设计](docs/35-海量数据架构设计.md) | 百万、千万、亿级容量规划、分片与分区、冷热分层 |
| 36 | [性能压测与Benchmark](docs/36-性能压测与Benchmark.md) | QPS、P50、P95、P99、插入压测、搜索压测 |
| 37 | [问题排查与Debug](docs/37-问题排查与Debug.md) | 连接失败、搜索为空、召回下降 |
| 38 | [源码阅读指南](docs/38-源码阅读指南.md) | 代码仓库结构、组件入口、请求链路 |
| 39 | [Milvus面试题大全](docs/39-Milvus面试题大全.md) | 基础题、架构题、索引题 |
| 40 | [未来趋势与生态](docs/40-未来趋势与生态.md) | Milvus 生态、向量数据库趋势、多模态趋势 |

## Demo 总览

| Demo | 用途 | 启动方式 |
|---|---|---|
| `demos/basic-search` | 文本向量入库与 TopK 检索 | `python main.py` |
| `demos/hybrid-search` | 多向量字段 Hybrid Search 与 RRF | `python main.py` |
| `demos/rag-system` | PDF/文本入库、召回、Rerank、LLM 回答 | `uvicorn main:app --reload --port 8001` |
| `demos/image-search` | CLIP 图片检索与 Web Demo | `uvicorn app:app --reload --port 8002` |
| `demos/multimodal-search` | 文搜图、图搜图、多模态检索 | `uvicorn app:app --reload --port 8003` |
| `demos/fastapi-service` | Milvus 检索服务 API | `uvicorn app:app --reload --port 8000` |
| `demos/benchmark` | 插入与搜索压测 | `python benchmark.py` |

## 常用命令

```bash
# 启动 Milvus
./scripts/start.sh

# 停止 Milvus
./scripts/stop.sh

# 查看健康状态
curl http://localhost:9091/healthz

# 运行基础搜索 Demo
cd demos/basic-search
cp .env.example .env
python main.py

# 运行 RAG API
cd demos/rag-system
cp .env.example .env
uvicorn main:app --reload --port 8001
```
