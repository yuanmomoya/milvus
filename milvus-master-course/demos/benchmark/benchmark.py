"""Milvus 性能压测工具

测试向量写入吞吐和搜索性能（QPS、P50/P95/P99 延迟）。
支持 HNSW 和 IVF_FLAT 两种索引，可配置数据量、维度和并发度。
对应教程第 36 章《性能压测与 Benchmark》。

用法: python benchmark.py --rows 100000 --dim 768 --index HNSW --concurrency 4
"""
from __future__ import annotations

import argparse
import logging
import os
import random
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any


def load_dotenv_if_available() -> None:
    """加载 .env；未安装 python-dotenv 时仍允许 --help 等轻量命令运行。"""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv()


load_dotenv_if_available()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)s %(name)s - %(message)s")
logger = logging.getLogger("benchmark")

np: Any = None
DataType: Any = None
MilvusClient: Any = None


@dataclass(frozen=True)
class BenchConfig:
    """压测配置"""
    uri: str
    token: str
    collection: str
    rows: int          # 写入数据量
    dim: int           # 向量维度
    batch_size: int    # 写入批大小
    index: str         # 索引类型：HNSW 或 IVF_FLAT
    concurrency: int   # 搜索并发度
    searches: int      # 搜索请求总数
    top_k: int         # 每次搜索返回数量


def random_vectors(rows: int, dim: int) -> np.ndarray:
    """生成随机归一化向量（模拟真实 Embedding 输出）"""
    if np is None:
        raise RuntimeError("请先调用 ensure_dependencies() 加载 numpy")
    vectors = np.random.random((rows, dim)).astype("float32")
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / np.maximum(norms, 1e-12)


def ensure_dependencies() -> None:
    """延迟加载压测依赖，让 --help 等命令不受运行时依赖影响。"""
    global DataType, MilvusClient, np

    try:
        import numpy as numpy_module
        from pymilvus import DataType as MilvusDataType
        from pymilvus import MilvusClient as Client
    except ImportError as exc:
        raise RuntimeError("缺少压测依赖，请先执行 pip install -r requirements.txt") from exc

    np = numpy_module
    DataType = MilvusDataType
    MilvusClient = Client


def ensure_collection(client: MilvusClient, cfg: BenchConfig) -> None:
    """创建压测用 Collection（每次重建保证环境干净）"""
    if client.has_collection(cfg.collection):
        client.drop_collection(cfg.collection)

    schema = MilvusClient.create_schema(auto_id=False, enable_dynamic_field=False)
    schema.add_field("id", DataType.INT64, is_primary=True)
    schema.add_field("tenant", DataType.VARCHAR, max_length=64)
    schema.add_field("embedding", DataType.FLOAT_VECTOR, dim=cfg.dim)

    # 根据配置选择索引类型
    index_params = MilvusClient.prepare_index_params()
    if cfg.index.upper() == "IVF_FLAT":
        index_params.add_index("embedding", index_type="IVF_FLAT", metric_type="COSINE", params={"nlist": 1024})
    else:
        index_params.add_index("embedding", index_type="HNSW", metric_type="COSINE", params={"M": 16, "efConstruction": 128})

    client.create_collection(cfg.collection, schema=schema, index_params=index_params)
    client.load_collection(cfg.collection)


def insert_rows(client: MilvusClient, cfg: BenchConfig) -> float:
    """批量写入数据，返回总耗时（秒）"""
    vectors = random_vectors(cfg.rows, cfg.dim)
    start = time.perf_counter()
    for offset in range(0, cfg.rows, cfg.batch_size):
        end = min(offset + cfg.batch_size, cfg.rows)
        rows = [
            {"id": row_id, "tenant": f"tenant-{row_id % 10}", "embedding": vectors[row_id].tolist()}
            for row_id in range(offset, end)
        ]
        client.insert(cfg.collection, rows)
    elapsed = time.perf_counter() - start
    logger.info("写入完成: %d 条, 耗时 %.2fs, 吞吐 %.0f rows/s", cfg.rows, elapsed, cfg.rows / elapsed)
    return elapsed


def one_search(client: MilvusClient, cfg: BenchConfig) -> float:
    """执行单次搜索，返回延迟（毫秒）"""
    vector = random_vectors(1, cfg.dim)[0].tolist()
    # 根据索引类型选择搜索参数
    params: dict[str, Any]
    if cfg.index.upper() == "IVF_FLAT":
        params = {"metric_type": "COSINE", "params": {"nprobe": 16}}
    else:
        params = {"metric_type": "COSINE", "params": {"ef": 64}}
    start = time.perf_counter()
    client.search(
        collection_name=cfg.collection,
        data=[vector],
        anns_field="embedding",
        search_params=params,
        limit=cfg.top_k,
        output_fields=["tenant"],
    )
    return (time.perf_counter() - start) * 1000


def percentile(values: list[float], pct: float) -> float:
    """计算百分位数"""
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(int(len(ordered) * pct), len(ordered) - 1)
    return ordered[index]


def run_searches(client: MilvusClient, cfg: BenchConfig) -> dict[str, float]:
    """并发搜索压测，返回 QPS 和延迟百分位"""
    # 预热：避免首次加载和缓存导致结果失真
    for _ in range(min(10, cfg.searches)):
        one_search(client, cfg)

    latencies: list[float] = []
    errors = 0
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=cfg.concurrency) as pool:
        futures = [pool.submit(one_search, client, cfg) for _ in range(cfg.searches)]
        for future in as_completed(futures):
            try:
                latencies.append(future.result())
            except Exception as exc:
                errors += 1
                logger.warning("搜索请求失败: %s", exc)
    elapsed = time.perf_counter() - start
    if errors:
        logger.warning("搜索阶段失败请求: %d/%d", errors, cfg.searches)
    if not latencies:
        raise RuntimeError("所有搜索请求均失败，无法计算性能指标")

    return {
        "qps": cfg.searches / elapsed,
        "p50_ms": statistics.median(latencies),
        "p95_ms": percentile(latencies, 0.95),
        "p99_ms": percentile(latencies, 0.99),
    }


def parse_args() -> BenchConfig:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="Milvus 性能压测工具")
    parser.add_argument("--uri", default=os.getenv("MILVUS_URI", "http://localhost:19530"))
    parser.add_argument("--token", default=os.getenv("MILVUS_TOKEN", ""))
    parser.add_argument("--collection", default=os.getenv("COLLECTION_NAME", "course_benchmark"))
    parser.add_argument("--rows", type=int, default=10000, help="写入数据量")
    parser.add_argument("--dim", type=int, default=384, help="向量维度")
    parser.add_argument("--batch-size", type=int, default=500, help="写入批大小")
    parser.add_argument("--index", choices=["HNSW", "IVF_FLAT"], default="HNSW", help="索引类型")
    parser.add_argument("--concurrency", type=int, default=4, help="搜索并发度")
    parser.add_argument("--searches", type=int, default=100, help="搜索请求总数")
    parser.add_argument("--top-k", type=int, default=10, help="TopK")
    args = parser.parse_args()
    return BenchConfig(
        uri=args.uri, token=args.token, collection=args.collection,
        rows=args.rows, dim=args.dim, batch_size=args.batch_size,
        index=args.index, concurrency=args.concurrency,
        searches=args.searches, top_k=args.top_k,
    )


def main() -> None:
    cfg = parse_args()
    ensure_dependencies()
    random.seed(42)
    np.random.seed(42)
    client = MilvusClient(uri=cfg.uri, token=cfg.token or None)

    print(f"=== Milvus Benchmark ===")
    print(f"数据量: {cfg.rows}, 维度: {cfg.dim}, 索引: {cfg.index}, 并发: {cfg.concurrency}")
    print()

    # 写入压测
    ensure_collection(client, cfg)
    insert_seconds = insert_rows(client, cfg)

    # 搜索压测
    metrics = run_searches(client, cfg)

    # 输出结果
    print(f"\n=== 结果 ===")
    print(f"写入: {cfg.rows} 条, 耗时 {insert_seconds:.2f}s, 吞吐 {cfg.rows/insert_seconds:.0f} rows/s")
    print(f"搜索: QPS={metrics['qps']:.1f}, P50={metrics['p50_ms']:.2f}ms, P95={metrics['p95_ms']:.2f}ms, P99={metrics['p99_ms']:.2f}ms")


if __name__ == "__main__":
    main()
