"""benchmark.py 单元测试：percentile 计算与 BenchConfig 数据结构。"""
from __future__ import annotations

import dataclasses

from benchmark import BenchConfig, percentile


class TestPercentile:
    """percentile 应正确计算百分位数。"""

    def test_empty_list_returns_zero(self) -> None:
        assert percentile([], 0.5) == 0.0

    def test_single_value(self) -> None:
        assert percentile([42.0], 0.5) == 42.0
        assert percentile([42.0], 0.99) == 42.0

    def test_p50_median(self) -> None:
        values = [1.0, 2.0, 3.0, 4.0, 5.0]
        result = percentile(values, 0.5)
        assert result == 3.0

    def test_p95(self) -> None:
        values = list(range(1, 101))
        result = percentile([float(v) for v in values], 0.95)
        assert result == 96.0

    def test_p99(self) -> None:
        values = list(range(1, 101))
        result = percentile([float(v) for v in values], 0.99)
        assert result == 100.0

    def test_unsorted_input(self) -> None:
        values = [5.0, 1.0, 3.0, 2.0, 4.0]
        result = percentile(values, 0.5)
        assert result == 3.0

    def test_p0_returns_minimum(self) -> None:
        values = [10.0, 20.0, 30.0]
        assert percentile(values, 0.0) == 10.0

    def test_does_not_mutate_input(self) -> None:
        values = [3.0, 1.0, 2.0]
        original = values.copy()
        percentile(values, 0.5)
        assert values == original

    def test_two_values(self) -> None:
        values = [10.0, 20.0]
        p50 = percentile(values, 0.5)
        assert p50 == 20.0

    def test_identical_values(self) -> None:
        values = [7.0, 7.0, 7.0, 7.0]
        assert percentile(values, 0.5) == 7.0
        assert percentile(values, 0.99) == 7.0


class TestBenchConfig:
    """BenchConfig frozen dataclass 基本行为。"""

    def test_create_config(self) -> None:
        cfg = BenchConfig(
            uri="http://localhost:19530", token="", collection="test",
            rows=1000, dim=128, batch_size=100,
            index="HNSW", concurrency=2, searches=50, top_k=10,
        )
        assert cfg.rows == 1000
        assert cfg.dim == 128
        assert cfg.index == "HNSW"

    def test_frozen(self) -> None:
        cfg = BenchConfig(
            uri="x", token="", collection="c",
            rows=1, dim=1, batch_size=1,
            index="HNSW", concurrency=1, searches=1, top_k=1,
        )
        try:
            cfg.rows = 9999  # type: ignore[misc]
            raise AssertionError("BenchConfig 应为 frozen dataclass")
        except dataclasses.FrozenInstanceError:
            pass
