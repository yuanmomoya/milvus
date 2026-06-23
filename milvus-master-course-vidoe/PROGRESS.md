# 视频生成进度

最近更新：2026-06-22

## 状态说明

| 标记 | 含义 |
|------|------|
| ✏️ | 旁白已写 |
| 🎙️ | TTS 已生成 |
| 🎬 | HTML 已生成 |
| ✅ | 渲染完成 |

## 章节进度

| # | 目录名 | 对应文档 | 状态 |
|---|--------|----------|------|
| 00 | chapter-00-course-overview | 00-教程规划与学习路径 | ✅ 已完成 |
| 01 | chapter-01-vector-database-basics | 01-向量数据库基础 | ✅ 已完成 |
| 02 | chapter-02-milvus-architecture | 02-Milvus整体架构 | ✅ 已完成 |
| 03 | chapter-03-quick-start | 03-Milvus快速开始 | ✅ 已完成 |
| 04 | chapter-04-docker-deploy | 04-Docker部署Milvus | ✅ 已完成 |
| 05 | chapter-05-pymilvus-guide | 05-pymilvus完全指南 | ✅ 已完成 |
| 06 | chapter-06-collection-design | 06-Collection设计 | ✅ 已完成 |
| 07 | chapter-07-vector-data-modeling | 07-向量数据建模 | ✅ 已完成 |
| 08 | chapter-08-embedding-models | 08-Embedding模型详解 | ✅ 已完成 |
| 09 | chapter-09-vector-index-theory | 09-向量索引原理 | ✅ 已完成 |
| 10 | chapter-10-ivf-index | 10-IVF原理与实战 | ✅ 已完成 |
| 11 | chapter-11-hnsw-index | 11-HNSW原理与实战 | ✅ 已完成 |
| 12 | chapter-12-pq-quantization | 12-PQ与量化压缩 | ✅ 已完成 |
| 13 | chapter-13-hybrid-search | 13-混合检索HybridSearch | ✅ 已完成 |
| 14 | chapter-14-scalar-filter | 14-标量过滤ScalarFilter | ✅ 已完成 |
| 15 | chapter-15-partition-design | 15-分区Partition设计 | ✅ 已完成 |
| 16 | chapter-16-batch-write | 16-批量写入优化 | ✅ 已完成 |
| 17 | chapter-17-query-tuning | 17-查询性能调优 | ✅ 已完成 |
| 18 | chapter-18-cluster-deploy | 18-Milvus集群部署 | ✅ 已完成 |
| 19 | chapter-19-high-availability | 19-Milvus高可用设计 | ✅ 已完成 |
| 20 | chapter-20-monitoring | 20-Milvus监控体系 | ✅ 已完成 |
| 21 | chapter-21-production-best-practices | 21-Milvus生产最佳实践 | ✅ 已完成 |
| 22 | chapter-22-rag-basics | 22-RAG架构基础 | ✅ 已完成 |
| 23 | chapter-23-rag-knowledge-base | 23-RAG知识库实战 | ✅ 已完成 |
| 24 | chapter-24-rag-retrieval-optimization | 24-RAG召回优化 | ✅ 已完成 |
| 25 | chapter-25-rerank | 25-Rerank重排序 | ✅ 已完成 |
| 26 | chapter-26-multi-route-retrieval | 26-多路召回架构 | ✅ 已完成 |
| 27 | chapter-27-agent-milvus | 27-Agent结合Milvus | ✅ 已完成 |
| 28 | chapter-28-langchain-integration | 28-LangChain集成 | ✅ 已完成 |
| 29 | chapter-29-llamaindex-integration | 29-LlamaIndex集成 | ✅ 已完成 |
| 30 | chapter-30-image-search | 30-图片检索系统 | ✅ 已完成 |
| 31 | chapter-31-clip-multimodal | 31-CLIP多模态检索 | ✅ 已完成 |
| 32 | chapter-32-video-search | 32-视频检索思路 | ✅ 已完成 |
| 33 | chapter-33-fastapi-development | 33-FastAPI接口开发 | ✅ 已完成 |
| 34 | chapter-34-ai-search-system | 34-构建完整AI搜索系统 | ✅ 已完成 |
| 35 | chapter-35-massive-data-architecture | 35-海量数据架构设计 | ✅ 已完成 |
| 36 | chapter-36-benchmark | 36-性能压测与Benchmark | ✅ 已完成 |
| 37 | chapter-37-troubleshooting | 37-问题排查与Debug | ✅ 已完成 |
| 38 | chapter-38-source-code-guide | 38-源码阅读指南 | ✅ 已完成 |
| 39 | chapter-39-interview-questions | 39-Milvus面试题大全 | ✅ 已完成 |
| 40 | chapter-40-future-trends | 40-未来趋势与生态 | ✅ 已完成 |

## 已完成步骤

1. ✅ 旁白文本与 storyboard（41/41）
2. ✅ TTS 音频生成（41/41）— `narration.mp3` + `narration_timing.json`
3. ✅ 分镜驱动 HTML（41/41）— `index.html` + GSAP + 字幕
4. ✅ 视频渲染（41/41）— 1920×1080、30fps、H.264 + AAC
5. ✅ 全量校验（41/41）— 失败 0，音视频总时长约 119.8 分钟，文件约 0.40 GiB

## 渲染命令

```bash
cd milvus-master-course-vidoe
conda activate test
export DOUBAO_TTS_API_KEY="有效的豆包 Key"

# 完整流水线；已有且有效的产物会跳过
python batch_generate_videos.py --phase all --continue-on-error

# 仅重新渲染视频
python batch_generate_videos.py --phase render --continue-on-error
```
