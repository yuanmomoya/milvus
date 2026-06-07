# Milvus 从入门到精通

一套完整的中文 Milvus 教学体系，包含 **40 章 Markdown 教程**、**7 个可运行 Demo**、**完整 Docker Compose 部署栈**，以及配套的 **41 集 HyperFrames 视频系列**（含字幕、TTS 旁白）。

## 仓库结构

```
milvus/
├── milvus教程大纲.md            # 教程总纲（输入 prompt）
├── CLAUDE.md                    # Claude Code 工作指引
├── milvus-master-course/        # 子项目一：教程代码 + 文档 + Demo
└── milvus-master-course-vidoe/  # 子项目二：HyperFrames 视频脚本 + TTS 工具
```

两个子项目相互独立，命令均需进入对应目录后执行。

## 子项目一：`milvus-master-course/`

教程文档、可运行 Demo 和 Docker Compose 部署栈。

```
milvus-master-course/
├── README.md
├── requirements.txt
├── docker-compose.yml
├── configs/milvus.yaml
├── docs/                # 00-40 章 Markdown 教程
├── demos/               # 7 个独立 Demo
│   ├── basic-search/
│   ├── hybrid-search/
│   ├── rag-system/
│   ├── image-search/
│   ├── multimodal-search/
│   ├── fastapi-service/
│   └── benchmark/
└── scripts/             # start.sh / stop.sh / init_data.py / benchmark.py
```

### 章节学习路径

| 阶段     | 章节  | 学完后能做什么                                  |
| -------- | ----- | ----------------------------------------------- |
| 基础     | 01-05 | 解释向量检索、启动 Milvus、完成 CRUD/Search     |
| 建模     | 06-09 | 设计 Collection、字段、Embedding 与索引         |
| 调优     | 10-17 | 选 IVF/HNSW/PQ，调 nprobe/ef/batch              |
| 生产     | 18-21 | 集群部署、高可用、监控、容量规划                |
| RAG      | 22-29 | 知识库问答、召回优化、Rerank、LangChain/LlamaIndex |
| 多模态   | 30-34 | 图片检索、CLIP、视频检索、AI 搜索 API           |
| 深水区   | 35-40 | 亿级架构、Benchmark、Debug、源码、面试          |

### 快速开始

```bash
cd milvus-master-course
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# 启动 Milvus（etcd + MinIO + standalone）
./scripts/start.sh
curl http://localhost:9091/healthz   # 健康检查
python scripts/init_data.py           # 写入示例数据

# 跑一个 Demo
cd demos/basic-search && cp .env.example .env && python main.py

# 跑 RAG API
cd demos/rag-system && cp .env.example .env && uvicorn main:app --reload --port 8001

# 压测
cd demos/benchmark && python benchmark.py --rows 10000 --dim 384 --index HNSW --concurrency 4
```

### 技术栈

| 组件             | 版本    | 说明                                           |
| ---------------- | ------- | ---------------------------------------------- |
| Milvus           | 2.6.15  | Docker Compose Standalone，生产章节扩展到集群  |
| pymilvus         | 2.6.12  | 仅使用 `MilvusClient` 高阶 API，不用旧版 ORM   |
| Python           | 3.11    | 全部 Demo 统一 Python 版本                     |
| Embedding        | bge-small-zh-v1.5 / CLIP | 文本 384 维，多模态用 CLIP |
| FastAPI          | 0.115.x | API 服务                                       |
| LangChain        | 0.3.x   | RAG 编排                                       |
| LLM              | OpenAI Compatible | 适配 Ollama / vLLM / 远程 API         |

### Docker 服务

| 服务              | 端口                       | 用途                       |
| ----------------- | -------------------------- | -------------------------- |
| Milvus standalone | 19530 (gRPC) / 9091 (健康) | 向量数据库                 |
| MinIO             | 9000 (API) / 9001 (Console) | Segment 对象存储          |
| etcd              | 2379（仅内部）             | 元数据协调                 |

## 子项目二：`milvus-master-course-vidoe/`

每章一个 HyperFrames 视频，统一的深色科技风设计、自动字幕、豆包 TTS 中文旁白。

```
milvus-master-course-vidoe/
├── VIDEO_GUIDE.md           # 视频制作唯一参考（设计系统 + 工作流 + TTS API）
├── PROGRESS.md              # 41 章进度追踪
├── doubao_tts.py            # 豆包 TTS 单段合成
├── build_narration.py       # 批量逐段 TTS + 拼接 + 时长 JSON
├── gen_all_chapters.py      # 按 timing.json 批量生成 index.html（含字幕层）
├── render_all.sh            # 批量渲染 mp4（已有的跳过）
└── chapter-00-course-overview/ ... chapter-40-future-trends/
```

### 制作流水线

```
narration.txt
  → build_narration.py（豆包 TTS）
  → narration.mp3 + narration_timing.json
  → gen_all_chapters.py
  → index.html（HyperFrames 脚本，含字幕层 + GSAP 时间轴）
  → npx hyperframes render
  → chapter-XX.mp4
```

### 常用命令

```bash
cd milvus-master-course-vidoe

# 1. 写完旁白后批量生成 TTS 与时间轴
python3 build_narration.py

# 2. 按时间轴批量生成 HTML（含字幕）
python3 gen_all_chapters.py

# 3. 渲染（HyperFrames 必须 Node 22）
source ~/.nvm/nvm.sh && nvm use 22
bash render_all.sh        # 批量；已渲染的章节会跳过

# 单章渲染：
cd chapter-01-vector-database-basics
npx hyperframes render --output chapter-01.mp4
```

### 每章产物

| 文件                     | 说明                                       |
| ------------------------ | ------------------------------------------ |
| `narration.txt`          | 旁白源文本（段落按空行分隔，一段一 scene） |
| `narration.mp3`          | TTS 音频                                   |
| `narration_timing.json`  | 各 scene 起止时间，驱动 HTML 与字幕        |
| `index.html`             | HyperFrames composition（场景 + GSAP）     |
| `chapter-XX.mp4`         | 最终渲染视频                               |

### 视频风格

- 深色科技感配色（深夜蓝 `#0f1729` + 青绿/紫色高亮）
- 每场景 8-15 秒，全章 90-200 秒
- 中文优先，旁白逐句字幕（底部固定半透明条）
- 详见 `milvus-master-course-vidoe/VIDEO_GUIDE.md`

## 章节总览

| 序号 | 章节                  | 序号 | 章节                  |
| ---: | --------------------- | ---: | --------------------- |
| 00   | 教程规划与学习路径    | 21   | Milvus 生产最佳实践   |
| 01   | 向量数据库基础        | 22   | RAG 架构基础          |
| 02   | Milvus 整体架构       | 23   | RAG 知识库实战        |
| 03   | Milvus 快速开始       | 24   | RAG 召回优化          |
| 04   | Docker 部署 Milvus    | 25   | Rerank 重排序         |
| 05   | pymilvus 完全指南     | 26   | 多路召回架构          |
| 06   | Collection 设计       | 27   | Agent 结合 Milvus     |
| 07   | 向量数据建模          | 28   | LangChain 集成        |
| 08   | Embedding 模型详解    | 29   | LlamaIndex 集成       |
| 09   | 向量索引原理          | 30   | 图片检索系统          |
| 10   | IVF 原理与实战        | 31   | CLIP 多模态检索       |
| 11   | HNSW 原理与实战       | 32   | 视频检索思路          |
| 12   | PQ 与量化压缩         | 33   | FastAPI 接口开发      |
| 13   | 混合检索 HybridSearch | 34   | 构建完整 AI 搜索系统  |
| 14   | 标量过滤 ScalarFilter | 35   | 海量数据架构设计      |
| 15   | 分区 Partition 设计   | 36   | 性能压测与 Benchmark  |
| 16   | 批量写入优化          | 37   | 问题排查与 Debug      |
| 17   | 查询性能调优          | 38   | 源码阅读指南          |
| 18   | Milvus 集群部署       | 39   | Milvus 面试题大全     |
| 19   | Milvus 高可用设计     | 40   | 未来趋势与生态        |
| 20   | Milvus 监控体系       |      |                       |

## 约定

- Python 3.11 + `from __future__ import annotations`
- 配置用 frozen dataclass；Pydantic 仅用于 API 入参/出参
- 用 stdlib `logging`，不要 `print`
- 所有注释、文档、旁白均为中文
- 写入用 `upsert` + 内容哈希主键保证幂等
- 默认索引：HNSW + COSINE
