"""copy_videos_to_cn.py 单元测试：make_intro 简介生成。"""
from __future__ import annotations

from copy_videos_to_cn import make_intro


class TestMakeIntro:
    """make_intro 应从旁白首段生成章节简介。"""

    def test_basic_intro(self) -> None:
        narration = "这是第一段旁白，作为简介。\n\n这是第二段。\n\n这是第三段。"
        result = make_intro("01", "向量数据库基础", narration)
        assert result.startswith("第 01 章 · 向量数据库基础")
        assert "这是第一段旁白，作为简介。" in result

    def test_single_paragraph(self) -> None:
        narration = "只有一段内容。"
        result = make_intro("05", "索引类型", narration)
        assert "只有一段内容。" in result
        assert "第 05 章" in result

    def test_empty_narration(self) -> None:
        result = make_intro("10", "性能优化", "")
        assert "第 10 章 · 性能优化" in result

    def test_uses_first_paragraph_only(self) -> None:
        narration = "首段重要内容。\n\n第二段不应出现。"
        result = make_intro("02", "搜索", narration)
        assert "首段重要内容。" in result
        assert "第二段不应出现" not in result

    def test_format(self) -> None:
        result = make_intro("03", "距离度量", "开头内容。\n\n后续。")
        assert result.endswith("\n")
