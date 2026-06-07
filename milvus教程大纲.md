~~~text
你是一名资深 AI 基础设施工程师、向量数据库专家、RAG 架构师，同时也是一名拥有多年教学经验的技术作者。

现在请你为我编写一整套《Milvus 从入门到精通》的完整教程体系。

# 教程目标

目标读者：
- Python 开发者
- AI 应用开发者
- RAG 工程师
- 搜索系统工程师
- LLM 应用开发者
- 后端工程师
- 希望系统掌握向量数据库的学习者

读者基础：
- 具备 Python 基础
- 了解基础数据库概念
- 不要求提前掌握向量数据库

最终学习目标：
读者完成本教程后，能够：
1. 理解向量数据库原理
2. 深入掌握 Milvus 架构与核心机制
3. 熟练使用 pymilvus 开发业务系统
4. 能独立开发 RAG 系统
5. 能独立开发图片/多模态检索系统
6. 能完成生产级 Milvus 部署与调优
7. 能处理海量向量数据场景
8. 理解 ANN / HNSW / IVF / PQ 等核心算法
9. 能进行性能优化与问题排查
10. 能结合 LangChain / LlamaIndex / FastAPI 等构建 AI 应用

---

# 技术要求（非常重要）

1. Milvus 使用“当前稳定最新版”
2. Python 统一使用 Python 3.11
3. 所有代码必须可运行
4. 所有代码必须有中文注释
5. 优先使用：
   - pymilvus
   - Docker Compose
   - FastAPI
   - LangChain
   - sentence-transformers
   - OpenAI Compatible API
6. 所有依赖版本必须明确
7. 所有目录结构必须完整
8. 每个 Demo 都必须能本地启动
9. Linux / macOS / Windows 都要兼容
10. 必须体现真实工程实践

---

# 输出要求

请生成一整套教程项目。

输出形式：
- 按章节拆分多个 Markdown 文件
- 每章一个独立 `.md`
- 同时生成：
  - README.md
  - requirements.txt
  - docker-compose.yml
  - demo 项目结构
  - 配置文件示例
  - 启动脚本
  - API 示例
  - curl 示例

---

# 教程风格要求

教程必须：
- 极其系统化
- 极其工程化
- 极其详细
- 由浅入深
- 图文并茂
- 大量 Mermaid 图
- 大量流程图
- 大量架构图
- 大量真实案例
- 每章包含：
  - 学习目标
  - 核心概念
  - 原理讲解
  - 完整代码
  - Demo
  - 图解
  - 常见错误
  - 面试题
  - 练习题
  - 小结

不要只讲 API。
必须讲：
- 为什么这样设计
- 底层原理
- 性能影响
- 生产问题
- 方案对比
- 最佳实践

---

# 教程目录（必须详细）

请按以下结构生成。

```bash
milvus-master-course/
│
├── README.md
├── requirements.txt
├── docker-compose.yml
├── docs/
│
│   ├── 01-向量数据库基础.md
│   ├── 02-Milvus整体架构.md
│   ├── 03-Milvus快速开始.md
│   ├── 04-Docker部署Milvus.md
│   ├── 05-pymilvus完全指南.md
│   ├── 06-Collection设计.md
│   ├── 07-向量数据建模.md
│   ├── 08-Embedding模型详解.md
│   ├── 09-向量索引原理.md
│   ├── 10-IVF原理与实战.md
│   ├── 11-HNSW原理与实战.md
│   ├── 12-PQ与量化压缩.md
│   ├── 13-混合检索HybridSearch.md
│   ├── 14-标量过滤ScalarFilter.md
│   ├── 15-分区Partition设计.md
│   ├── 16-批量写入优化.md
│   ├── 17-查询性能调优.md
│   ├── 18-Milvus集群部署.md
│   ├── 19-Milvus高可用设计.md
│   ├── 20-Milvus监控体系.md
│   ├── 21-Milvus生产最佳实践.md
│   ├── 22-RAG架构基础.md
│   ├── 23-RAG知识库实战.md
│   ├── 24-RAG召回优化.md
│   ├── 25-Rerank重排序.md
│   ├── 26-多路召回架构.md
│   ├── 27-Agent结合Milvus.md
│   ├── 28-LangChain集成.md
│   ├── 29-LlamaIndex集成.md
│   ├── 30-图片检索系统.md
│   ├── 31-CLIP多模态检索.md
│   ├── 32-视频检索思路.md
│   ├── 33-FastAPI接口开发.md
│   ├── 34-构建完整AI搜索系统.md
│   ├── 35-海量数据架构设计.md
│   ├── 36-性能压测与Benchmark.md
│   ├── 37-问题排查与Debug.md
│   ├── 38-源码阅读指南.md
│   ├── 39-Milvus面试题大全.md
│   └── 40-未来趋势与生态.md
│
├── demos/
│
│   ├── basic-search/
│   ├── hybrid-search/
│   ├── rag-system/
│   ├── image-search/
│   ├── multimodal-search/
│   ├── fastapi-service/
│   └── benchmark/
│
├── scripts/
│   ├── start.sh
│   ├── stop.sh
│   ├── init_data.py
│   └── benchmark.py
│
└── assets/
    ├── architecture/
    ├── diagrams/
    └── screenshots/
~~~

------

# 重点章节要求（必须重点展开）

# 一、向量数据库底层原理

必须详细讲：

- 向量是什么
- Embedding 原理
- 余弦相似度
- L2 距离
- ANN
- 暴力检索 vs ANN
- HNSW 图结构
- IVF 聚类
- PQ 压缩
- Recall / QPS / Latency
- 向量维度影响
- 内存布局
- 索引构建成本

必须配 Mermaid 图。

------

# 二、Milvus 架构

必须详细讲：

- Proxy
- QueryNode
- DataNode
- RootCoord
- QueryCoord
- IndexNode
- etcd
- MinIO
- Pulsar

讲清：

- 数据流
- 查询流
- 写入流程
- Segment 生命周期
- Flush
- Compaction
- WAL

必须有架构图。

------

# 三、RAG 实战（重点）

必须实现完整生产级 RAG 系统：

包含：

- PDF 解析
- 文档切块
- Chunk 策略
- Embedding
- 向量入库
- Query Rewrite
- Recall
- Rerank
- Prompt Template
- LLM Answer
- 引用来源
- 对话记忆
- 多轮问答

要求：

- 使用 Milvus
- 使用 LangChain
- 使用 FastAPI
- Python 3.11
- 完整项目结构
- 支持 OpenAI Compatible API

必须讲：

- 为什么 Chunk 很重要
- Chunk Size 如何影响召回
- 如何提升 Recall
- 如何降低幻觉
- TopK 如何选择

------

# 四、图片检索系统（重点）

必须实现：

- 图片 Embedding
- CLIP 模型
- 图搜图
- 文搜图
- 多模态搜索
- TopK 检索
- 相似度排序

要求：

- 使用 transformers
- 使用 PIL
- 使用 torch
- 使用 Milvus

必须包含：

- 数据集准备
- 批量导入
- 检索 API
- Web Demo

------

# 五、生产级内容（重点）

必须详细讲：

- 百万级向量
- 千万级向量
- 亿级向量
- 分片设计
- 分区策略
- 热数据
- 冷数据
- 内存优化
- GPU 加速
- 集群扩容
- 查询调优
- Compaction
- Segment Merge
- 索引重建
- 容灾

------

# 六、性能优化（重点）

必须讲：

- nprobe
- efSearch
- efConstruction
- index_file_size
- batch insert
- query concurrency
- cache
- mmap

必须提供：

- Benchmark 脚本
- QPS 测试
- 延迟测试
- 参数对比表

------

# 七、工程实践（重点）

所有 Demo 必须：

- 有 requirements.txt
- 有 .env.example
- 有 docker-compose.yml
- 有 README.md
- 有 curl 示例
- 有 API 文档
- 有 启动步骤
- 有 项目结构说明

------

# 代码要求

所有代码必须：

- 使用 Python 3.11
- 使用类型注解
- 使用 dataclass（适合时）
- 有日志
- 有异常处理
- 有配置文件
- 有模块化结构
- 符合生产工程规范

------

# 图示要求

大量使用：

- Mermaid
- 架构图
- 流程图
- 时序图
- 数据流图

例如：

- 写入流程
- 查询流程
- Segment 生命周期
- HNSW 图
- RAG Flow
- 多模态流程

------

# 输出方式

请严格按以下步骤输出：

第一阶段：

1. 输出完整教程规划
2. 输出章节学习路径
3. 输出每章核心知识点
4. 输出项目整体架构

第二阶段：
逐章生成 Markdown 内容。

第三阶段：
生成 Demo 项目代码。

第四阶段：
生成部署与生产方案。

不要省略细节。
不要只给大纲。
必须是真正可落地的完整教程。

