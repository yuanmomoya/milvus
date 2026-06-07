# 36 性能压测与 Benchmark

## 学习目标

学完本章后，你应该能够：

- 设计向量搜索的性能压测方案。
- 使用脚本测量 QPS、延迟和召回率。
- 对比不同索引和参数配置的性能。
- 建立性能基线并持续跟踪。
- 解读压测结果并定位瓶颈。

---

## 压测指标

| 指标 | 含义 | 目标参考 |
|---|---|---|
| QPS | 每秒查询数 | 取决于业务并发 |
| P50 延迟 | 50% 请求的延迟 | < 10ms |
| P95 延迟 | 95% 请求的延迟 | < 30ms |
| P99 延迟 | 99% 请求的延迟 | < 100ms |
| Recall@K | 召回率 | > 95% |
| 写入吞吐 | 每秒写入行数 | > 10K rows/s |

---

## 压测脚本

```python
import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pymilvus import MilvusClient


@dataclass
class BenchmarkConfig:
    collection_name: str
    dim: int
    num_queries: int = 1000
    top_k: int = 10
    ef: int = 64
    concurrency: int = 1


@dataclass
class BenchmarkResult:
    qps: float
    p50_ms: float
    p95_ms: float
    p99_ms: float
    avg_ms: float
    total_queries: int
    errors: int


def run_search_benchmark(client: MilvusClient, config: BenchmarkConfig) -> BenchmarkResult:
    """搜索性能压测"""
    # 生成随机查询向量
    queries = np.random.randn(config.num_queries, config.dim).astype("float32")
    queries = queries / np.linalg.norm(queries, axis=1, keepdims=True)

    latencies = []
    errors = 0

    def single_search(query_vector):
        start = time.perf_counter()
        try:
            client.search(
                collection_name=config.collection_name,
                data=[query_vector.tolist()],
                anns_field="embedding",
                search_params={"metric_type": "COSINE", "params": {"ef": config.ef}},
                limit=config.top_k,
                output_fields=["id"],
            )
            return (time.perf_counter() - start) * 1000
        except Exception:
            return -1

    if config.concurrency == 1:
        for q in queries:
            lat = single_search(q)
            if lat >= 0:
                latencies.append(lat)
            else:
                errors += 1
    else:
        with ThreadPoolExecutor(max_workers=config.concurrency) as executor:
            futures = [executor.submit(single_search, q) for q in queries]
            for f in as_completed(futures):
                lat = f.result()
                if lat >= 0:
                    latencies.append(lat)
                else:
                    errors += 1

    total_time = sum(latencies) / 1000
    return BenchmarkResult(
        qps=len(latencies) / total_time if total_time > 0 else 0,
        p50_ms=np.percentile(latencies, 50),
        p95_ms=np.percentile(latencies, 95),
        p99_ms=np.percentile(latencies, 99),
        avg_ms=np.mean(latencies),
        total_queries=len(latencies),
        errors=errors,
    )


# 使用
client = MilvusClient(uri="http://localhost:19530")
config = BenchmarkConfig(collection_name="bench_collection", dim=768, num_queries=500, concurrency=4)
result = run_search_benchmark(client, config)
print(f"QPS={result.qps:.0f}  P50={result.p50_ms:.1f}ms  P95={result.p95_ms:.1f}ms  P99={result.p99_ms:.1f}ms")
```

---

## 召回率评测

```python
def benchmark_recall(client: MilvusClient, collection: str, dim: int, num_queries: int = 100, top_k: int = 10):
    """以 FLAT 结果为基准计算召回率"""
    queries = np.random.randn(num_queries, dim).astype("float32")
    queries = queries / np.linalg.norm(queries, axis=1, keepdims=True)

    recalls = []
    for q in queries:
        # FLAT 精确结果（需要一个 FLAT 索引的 Collection 作为基准）
        gt = client.search(
            collection_name=f"{collection}_flat",
            data=[q.tolist()], anns_field="embedding",
            search_params={"metric_type": "COSINE"}, limit=top_k, output_fields=["id"],
        )
        gt_ids = {hit["id"] for hit in gt[0]}

        # ANN 结果
        ann = client.search(
            collection_name=collection,
            data=[q.tolist()], anns_field="embedding",
            search_params={"metric_type": "COSINE", "params": {"ef": 64}}, limit=top_k, output_fields=["id"],
        )
        ann_ids = {hit["id"] for hit in ann[0]}

        recalls.append(len(gt_ids & ann_ids) / len(gt_ids))

    return {"recall@k": np.mean(recalls), "std": np.std(recalls)}
```

---

## 参数对比实验

```python
def parameter_sweep(client, collection, dim):
    """参数扫描：对比不同 ef 的性能"""
    print(f"{'ef':>6} | {'P50':>8} | {'P95':>8} | {'QPS':>8}")
    print("-" * 40)

    for ef in [16, 32, 64, 128, 256, 512]:
        config = BenchmarkConfig(
            collection_name=collection, dim=dim,
            num_queries=200, ef=ef, concurrency=1,
        )
        result = run_search_benchmark(client, config)
        print(f"{ef:>6} | {result.p50_ms:>6.1f}ms | {result.p95_ms:>6.1f}ms | {result.qps:>6.0f}")
```

典型输出：

```
    ef |      P50 |      P95 |      QPS
----------------------------------------
    16 |    1.8ms |    3.2ms |    480
    32 |    2.5ms |    4.1ms |    350
    64 |    4.2ms |    6.8ms |    210
   128 |    7.5ms |   12.3ms |    120
   256 |   14.1ms |   22.5ms |     65
   512 |   27.8ms |   43.2ms |     33
```

---

## 写入吞吐压测

```python
def benchmark_write(client: MilvusClient, collection: str, dim: int, total: int = 100000, batch_size: int = 1000):
    """写入吞吐压测"""
    start = time.perf_counter()
    written = 0

    for i in range(0, total, batch_size):
        size = min(batch_size, total - i)
        vectors = np.random.randn(size, dim).astype("float32")
        vectors = (vectors / np.linalg.norm(vectors, axis=1, keepdims=True)).tolist()
        data = [{"id": str(i+j), "embedding": vectors[j]} for j in range(size)]
        client.upsert(collection_name=collection, data=data)
        written += size

    elapsed = time.perf_counter() - start
    print(f"写入 {written} 条, 耗时 {elapsed:.1f}s, 吞吐 {written/elapsed:.0f} rows/s")
```

---

## 常见错误

| 现象 | 原因 | 修复 |
|---|---|---|
| 压测 QPS 远低于预期 | 单线程测试 | 增加并发度 |
| P99 远高于 P50 | GC 或 Compaction 干扰 | 避开 Compaction 时间段 |
| 召回率测试结果不稳定 | 查询向量太少 | 增加到 100+ 个查询 |
| 写入压测后搜索变慢 | 大量小 Segment | 等待 Compaction |

---

## 面试题

1. **为什么压测要关注 P95/P99 而不只是平均值？** 平均值会被大量快请求拉低，掩盖少数慢请求。P95/P99 反映尾部延迟，是用户体验的真实反映。

2. **如何确保压测结果可复现？** 固定随机种子、固定数据量、固定并发度、在相同硬件和负载条件下测试。记录完整的测试参数。

3. **并发压测时 QPS 为什么会有上限？** CPU 饱和、内存带宽饱和、或 Milvus 内部队列满。找到饱和点后继续加并发只会增加延迟不会增加 QPS。

---

## 练习题

1. 对 10 万条数据分别用 ef=32/64/128 压测，画出 ef-latency 和 ef-QPS 曲线。
2. 对比 1/4/8/16 并发下的 QPS 和 P95 延迟，找到吞吐饱和点。
3. 对比 HNSW 和 IVF_FLAT 在相同数据上的 QPS 和召回率。

---

## 小结

性能压测是调优的基础——没有数据就没有优化方向。核心流程：建立基线 → 参数扫描 → 找到最优配置 → 持续监控。关注 P95/P99 而非平均值，关注并发下的表现而非单线程。
