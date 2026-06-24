"""config.py 单元测试：Settings frozen dataclass 默认值与环境变量覆盖。

Settings 的默认值使用 os.getenv()，在类定义时求值，
因此测试环境变量覆盖需要先设好环境变量再 reload 模块。
"""
from __future__ import annotations

import dataclasses
import importlib
import os
from unittest.mock import patch

import config
from config import Settings


class TestSettingsDefaults:
    """未设环境变量时，Settings 应使用合理默认值。"""

    def test_default_milvus_uri(self) -> None:
        s = Settings()
        assert "localhost" in s.milvus_uri or "19530" in s.milvus_uri

    def test_default_collection_name(self) -> None:
        s = Settings()
        assert s.collection_name == "course_rag_chunks"

    def test_default_chunk_params(self) -> None:
        s = Settings()
        assert s.chunk_size == 600
        assert s.chunk_overlap == 100

    def test_default_search_params(self) -> None:
        s = Settings()
        assert s.top_k == 10
        assert s.rerank_top_n == 5

    def test_default_log_level(self) -> None:
        s = Settings()
        assert s.log_level == "INFO"

    def test_frozen(self) -> None:
        s = Settings()
        assert dataclasses.is_dataclass(s)
        try:
            s.milvus_uri = "http://other:19530"  # type: ignore[misc]
            raise AssertionError("Settings 应为 frozen dataclass")
        except dataclasses.FrozenInstanceError:
            pass


class TestSettingsEnvOverride:
    """环境变量应可覆盖默认值（需 reload 模块重新求值 os.getenv）。"""

    def test_override_collection_name(self) -> None:
        with patch.dict(os.environ, {"COLLECTION_NAME": "my_custom_col"}):
            importlib.reload(config)
            s = config.Settings()
            assert s.collection_name == "my_custom_col"

    def test_override_chunk_size(self) -> None:
        with patch.dict(os.environ, {"CHUNK_SIZE": "800"}):
            importlib.reload(config)
            s = config.Settings()
            assert s.chunk_size == 800

    def test_override_top_k(self) -> None:
        with patch.dict(os.environ, {"TOP_K": "20"}):
            importlib.reload(config)
            s = config.Settings()
            assert s.top_k == 20

    def test_override_log_level(self) -> None:
        with patch.dict(os.environ, {"LOG_LEVEL": "DEBUG"}):
            importlib.reload(config)
            s = config.Settings()
            assert s.log_level == "DEBUG"
