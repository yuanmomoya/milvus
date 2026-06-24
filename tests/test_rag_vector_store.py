"""vector_store.py 单元测试：stable_id 哈希与 Chunk 数据结构。"""
from __future__ import annotations

import hashlib

from vector_store import Chunk, stable_id


class TestStableId:
    """stable_id 应产生稳定、唯一的 SHA-1 主键。"""

    def test_deterministic(self) -> None:
        result_a = stable_id("doc.pdf", 1, 0, "你好世界")
        result_b = stable_id("doc.pdf", 1, 0, "你好世界")
        assert result_a == result_b

    def test_sha1_hex_format(self) -> None:
        result = stable_id("a.md", 0, 0, "text")
        assert len(result) == 40
        assert all(c in "0123456789abcdef" for c in result)

    def test_matches_manual_sha1(self) -> None:
        raw = "src.pdf:2:3:hello".encode("utf-8")
        expected = hashlib.sha1(raw).hexdigest()
        assert stable_id("src.pdf", 2, 3, "hello") == expected

    def test_different_source_different_id(self) -> None:
        assert stable_id("a.pdf", 0, 0, "text") != stable_id("b.pdf", 0, 0, "text")

    def test_different_page_different_id(self) -> None:
        assert stable_id("a.pdf", 0, 0, "text") != stable_id("a.pdf", 1, 0, "text")

    def test_different_chunk_id_different_id(self) -> None:
        assert stable_id("a.pdf", 0, 0, "text") != stable_id("a.pdf", 0, 1, "text")

    def test_different_text_different_id(self) -> None:
        assert stable_id("a.pdf", 0, 0, "foo") != stable_id("a.pdf", 0, 0, "bar")

    def test_unicode_text(self) -> None:
        result = stable_id("doc.pdf", 0, 0, "向量数据库是一种专门存储高维向量的数据库")
        assert len(result) == 40

    def test_empty_text(self) -> None:
        result = stable_id("doc.pdf", 0, 0, "")
        assert len(result) == 40


class TestChunk:
    """Chunk frozen dataclass 基本行为。"""

    def test_create_with_defaults(self) -> None:
        chunk = Chunk(text="内容", source="test.md")
        assert chunk.text == "内容"
        assert chunk.source == "test.md"
        assert chunk.page == 0
        assert chunk.chunk_id == 0

    def test_create_with_all_fields(self) -> None:
        chunk = Chunk(text="段落", source="file.pdf", page=5, chunk_id=3)
        assert chunk.page == 5
        assert chunk.chunk_id == 3

    def test_frozen_immutability(self) -> None:
        chunk = Chunk(text="a", source="b")
        import dataclasses
        assert dataclasses.is_dataclass(chunk)
        try:
            chunk.text = "changed"  # type: ignore[misc]
            raise AssertionError("应拒绝对 frozen dataclass 的赋值")
        except dataclasses.FrozenInstanceError:
            pass

    def test_equality(self) -> None:
        a = Chunk(text="x", source="y", page=1, chunk_id=2)
        b = Chunk(text="x", source="y", page=1, chunk_id=2)
        assert a == b

    def test_inequality(self) -> None:
        a = Chunk(text="x", source="y")
        b = Chunk(text="z", source="y")
        assert a != b
