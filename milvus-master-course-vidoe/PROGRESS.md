# 视频生成进度

生成时间：2026-05-23

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
| 01 | chapter-01-vector-database-basics | 01-向量数据库基础 | 🎬 待渲染 |
| 02 | chapter-02-milvus-architecture | 02-Milvus整体架构 | 🎬 待渲染 |
| 03 | chapter-03-quick-start | 03-Milvus快速开始 | 🎬 待渲染 |
| 04 | chapter-04-docker-deploy | 04-Docker部署Milvus | 🎬 待渲染 |
| 05 | chapter-05-pymilvus-guide | 05-pymilvus完全指南 | 🎬 待渲染 |
| 06 | chapter-06-collection-design | 06-Collection设计 | 🎬 待渲染 |
| 07 | chapter-07-vector-data-modeling | 07-向量数据建模 | 🎬 待渲染 |
| 08 | chapter-08-embedding-models | 08-Embedding模型详解 | 🎬 待渲染 |
| 09 | chapter-09-vector-index-theory | 09-向量索引原理 | 🎬 待渲染 |
| 10 | chapter-10-ivf-index | 10-IVF原理与实战 | 🎬 待渲染 |
| 11 | chapter-11-hnsw-index | 11-HNSW原理与实战 | 🎬 待渲染 |
| 12 | chapter-12-pq-quantization | 12-PQ与量化压缩 | 🎬 待渲染 |
| 13 | chapter-13-hybrid-search | 13-混合检索HybridSearch | 🎬 待渲染 |
| 14 | chapter-14-scalar-filter | 14-标量过滤ScalarFilter | 🎬 待渲染 |
| 15 | chapter-15-partition-design | 15-分区Partition设计 | 🎬 待渲染 |
| 16 | chapter-16-batch-write | 16-批量写入优化 | 🎬 待渲染 |
| 17 | chapter-17-query-tuning | 17-查询性能调优 | 🎬 待渲染 |
| 18 | chapter-18-cluster-deploy | 18-Milvus集群部署 | 🎬 待渲染 |
| 19 | chapter-19-high-availability | 19-Milvus高可用设计 | 🎬 待渲染 |
| 20 | chapter-20-monitoring | 20-Milvus监控体系 | 🎬 待渲染 |
| 21 | chapter-21-production-best-practices | 21-Milvus生产最佳实践 | 🎬 待渲染 |
| 22 | chapter-22-rag-basics | 22-RAG架构基础 | 🎬 待渲染 |
| 23 | chapter-23-rag-knowledge-base | 23-RAG知识库实战 | 🎬 待渲染 |
| 24 | chapter-24-rag-retrieval-optimization | 24-RAG召回优化 | 🎬 待渲染 |
| 25 | chapter-25-rerank | 25-Rerank重排序 | 🎬 待渲染 |
| 26 | chapter-26-multi-route-retrieval | 26-多路召回架构 | 🎬 待渲染 |
| 27 | chapter-27-agent-milvus | 27-Agent结合Milvus | 🎬 待渲染 |
| 28 | chapter-28-langchain-integration | 28-LangChain集成 | 🎬 待渲染 |
| 29 | chapter-29-llamaindex-integration | 29-LlamaIndex集成 | 🎬 待渲染 |
| 30 | chapter-30-image-search | 30-图片检索系统 | 🎬 待渲染 |
| 31 | chapter-31-clip-multimodal | 31-CLIP多模态检索 | 🎬 待渲染 |
| 32 | chapter-32-video-search | 32-视频检索思路 | 🎬 待渲染 |
| 33 | chapter-33-fastapi-development | 33-FastAPI接口开发 | 🎬 待渲染 |
| 34 | chapter-34-ai-search-system | 34-构建完整AI搜索系统 | 🎬 待渲染 |
| 35 | chapter-35-massive-data-architecture | 35-海量数据架构设计 | 🎬 待渲染 |
| 36 | chapter-36-benchmark | 36-性能压测与Benchmark | 🎬 待渲染 |
| 37 | chapter-37-troubleshooting | 37-问题排查与Debug | 🎬 待渲染 |
| 38 | chapter-38-source-code-guide | 38-源码阅读指南 | 🎬 待渲染 |
| 39 | chapter-39-interview-questions | 39-Milvus面试题大全 | 🎬 待渲染 |
| 40 | chapter-40-future-trends | 40-未来趋势与生态 | 🎬 待渲染 |

## 已完成步骤

1. ✅ 旁白文本编写（40/40）
2. ✅ TTS 音频生成（40/40）— narration.mp3 + narration_timing.json
3. ✅ HTML 视频脚本生成（40/40）— index.html with subtitles
4. ✅ 视频渲染（40/40）— chapter-XX.mp4，总计 427MB

## 渲染命令

```bash
source ~/.nvm/nvm.sh && nvm use 22
cd milvus-master-course-vidoe

for dir in chapter-*/; do
  echo "Rendering $dir..."
  cd "$dir"
  npx hyperframes render --output "$(basename $dir | sed 's/-[^-]*$//' | head -c 10).mp4"
  cd ..
done
```
