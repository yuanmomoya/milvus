"""generate_storyboards.py 单元测试：文本处理与分类纯函数。"""
from __future__ import annotations

from generate_storyboards import (
    VISUAL_SPECS,
    classify_visual,
    clean_title,
    purpose_for,
    short_point,
    split_sentences,
    toml_array,
    toml_string,
)


class TestSplitSentences:
    """split_sentences 应按中文句末标点拆分。"""

    def test_single_sentence(self) -> None:
        assert split_sentences("你好。") == ["你好。"]

    def test_multiple_sentences(self) -> None:
        result = split_sentences("第一句。第二句！第三句？")
        assert result == ["第一句。", "第二句！", "第三句？"]

    def test_strips_whitespace(self) -> None:
        result = split_sentences("  你好。  世界！  ")
        assert result == ["你好。", "世界！"]

    def test_empty_string(self) -> None:
        assert split_sentences("") == []

    def test_no_punctuation(self) -> None:
        assert split_sentences("没有标点") == ["没有标点"]

    def test_semicolon_split(self) -> None:
        result = split_sentences("第一部分；第二部分。")
        assert len(result) == 2


class TestCleanTitle:
    """clean_title 应从段落首句提取简短标题。"""

    def test_simple_title(self) -> None:
        assert clean_title("向量数据库简介。详细说明。") == "向量数据库简介"

    def test_removes_prefix(self) -> None:
        assert "先来" not in clean_title("先来了解一下基本概念。")

    def test_removes_last_chapter_prefix(self) -> None:
        result = clean_title("上一章讨论了索引。这一章讲搜索。")
        assert result == "这一章讲搜索"

    def test_truncates_long_title(self) -> None:
        long_text = "这是一个非常非常非常非常非常非常非常非常非常非常非常长的标题。"
        result = clean_title(long_text)
        assert len(result) <= 28
        assert result.endswith("…")

    def test_fallback_for_empty(self) -> None:
        assert clean_title("") == "核心概念"

    def test_strips_punctuation(self) -> None:
        result = clean_title("测试内容，")
        assert not result.endswith("，")


class TestShortPoint:
    """short_point 应生成简短要点摘要。"""

    def test_short_sentence_unchanged(self) -> None:
        assert short_point("简短要点") == "简短要点"

    def test_truncates_long_sentence(self) -> None:
        long = "这" * 50
        result = short_point(long, limit=42)
        assert len(result) <= 42
        assert result.endswith("…")

    def test_strips_punctuation(self) -> None:
        result = short_point("，测试内容。")
        assert not result.startswith("，")
        assert not result.endswith("。")

    def test_removes_filler_prefixes(self) -> None:
        assert "接下来" not in short_point("接下来我们看代码。")

    def test_custom_limit(self) -> None:
        result = short_point("a" * 20, limit=10)
        assert len(result) <= 10


class TestClassifyVisual:
    """classify_visual 应根据段落内容与场景位置选择视觉类型。"""

    def test_last_scene_is_recap(self) -> None:
        spec = classify_visual("任何内容", scene_index=5, scene_count=5)
        assert spec.visual_type == "recap"

    def test_first_scene_with_hook_words(self) -> None:
        spec = classify_visual("想象一下如果没有向量数据库", scene_index=1, scene_count=5)
        assert spec.visual_type == "hook-comparison"

    def test_first_scene_without_hook_words(self) -> None:
        spec = classify_visual("本章介绍基本概念", scene_index=1, scene_count=5)
        assert spec.visual_type == "learning-map"

    def test_hnsw_keyword(self) -> None:
        spec = classify_visual("HNSW 图索引的工作原理", scene_index=3, scene_count=5)
        assert spec.visual_type == "graph-search"

    def test_pq_keyword(self) -> None:
        spec = classify_visual("PQ 量化压缩可以降低内存", scene_index=2, scene_count=5)
        assert spec.visual_type == "compression"

    def test_ivf_keyword(self) -> None:
        spec = classify_visual("IVF 索引通过 nlist 参数聚类", scene_index=2, scene_count=5)
        assert spec.visual_type == "cluster-search"

    def test_code_keyword(self) -> None:
        spec = classify_visual("下面来看 python 代码演示", scene_index=3, scene_count=5)
        assert spec.visual_type == "code-terminal"

    def test_architecture_keyword(self) -> None:
        spec = classify_visual("Milvus 的 proxy 和 querynode 架构", scene_index=3, scene_count=5)
        assert spec.visual_type == "architecture"

    def test_dashboard_keyword(self) -> None:
        spec = classify_visual("关注 QPS 和 P99 延迟指标", scene_index=3, scene_count=5)
        assert spec.visual_type == "dashboard"

    def test_error_diagnosis_keyword(self) -> None:
        spec = classify_visual("常见的错误处理和排查方法", scene_index=3, scene_count=5)
        assert spec.visual_type == "error-diagnosis"

    def test_default_fallback(self) -> None:
        spec = classify_visual("普通内容没有匹配关键词", scene_index=3, scene_count=5)
        assert spec.visual_type in VISUAL_SPECS


class TestPurposeFor:
    """purpose_for 应根据内容和位置判定场景用途。"""

    def test_first_scene_is_hook(self) -> None:
        assert purpose_for("任何内容", scene_index=1, scene_count=5) == "hook"

    def test_last_scene_is_summary(self) -> None:
        assert purpose_for("任何内容", scene_index=5, scene_count=5) == "summary"

    def test_error_handling_is_diagnosis(self) -> None:
        assert purpose_for("错误处理和排查", scene_index=3, scene_count=5) == "diagnosis"

    def test_code_is_demo(self) -> None:
        assert purpose_for("代码实现演示", scene_index=3, scene_count=5) == "demo"

    def test_comparison_is_comparison(self) -> None:
        assert purpose_for("两者的区别和选择", scene_index=3, scene_count=5) == "comparison"

    def test_default_is_concept(self) -> None:
        assert purpose_for("向量空间的基本性质", scene_index=3, scene_count=5) == "concept"


class TestTomlString:
    """toml_string 应生成合法的 TOML 字符串字面量。"""

    def test_ascii(self) -> None:
        assert toml_string("hello") == '"hello"'

    def test_chinese(self) -> None:
        result = toml_string("向量数据库")
        assert result.startswith('"')
        assert result.endswith('"')
        assert "向量数据库" in result

    def test_quotes_escaped(self) -> None:
        result = toml_string('say "hi"')
        assert '\\"' in result

    def test_empty(self) -> None:
        assert toml_string("") == '""'


class TestTomlArray:
    """toml_array 应生成 TOML 数组字面量。"""

    def test_single_item(self) -> None:
        assert toml_array(["a"]) == '["a"]'

    def test_multiple_items(self) -> None:
        result = toml_array(["x", "y", "z"])
        assert result == '["x", "y", "z"]'

    def test_empty_list(self) -> None:
        assert toml_array([]) == "[]"

    def test_tuple_input(self) -> None:
        result = toml_array(("a", "b"))
        assert result == '["a", "b"]'

    def test_chinese_items(self) -> None:
        result = toml_array(["你好", "世界"])
        assert "你好" in result
        assert "世界" in result
