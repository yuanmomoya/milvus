"""gen_all_chapters.py 单元测试：文本拆分与标题提取。"""
from __future__ import annotations

from gen_all_chapters import extract_title, gen_scene_html, split_sentences


class TestSplitSentences:
    """split_sentences 按中文句末标点拆分。"""

    def test_basic(self) -> None:
        assert split_sentences("你好。世界！") == ["你好。", "世界！"]

    def test_strips_whitespace(self) -> None:
        result = split_sentences("  你好。  ")
        assert result == ["你好。"]

    def test_empty(self) -> None:
        assert split_sentences("") == []

    def test_no_punctuation(self) -> None:
        assert split_sentences("无标点文本") == ["无标点文本"]

    def test_question_mark(self) -> None:
        result = split_sentences("这是什么？那是什么？")
        assert len(result) == 2


class TestExtractTitle:
    """extract_title 应从段落提取简短标题。"""

    def test_short_first_sentence(self) -> None:
        assert extract_title("向量数据库。详细说明。") == "向量数据库"

    def test_truncates_at_20(self) -> None:
        long = "这是一段非常非常非常非常非常非常非常非常非常长的句子。"
        result = extract_title(long)
        assert len(result) <= 20

    def test_strips_trailing_punctuation(self) -> None:
        result = extract_title("测试标题。")
        assert not result.endswith("。")

    def test_no_punctuation_fallback(self) -> None:
        result = extract_title("没有标点的段落文本内容")
        assert len(result) <= 20

    def test_empty_string(self) -> None:
        result = extract_title("")
        assert result == ""


class TestGenSceneHtml:
    """gen_scene_html 应生成包含正确结构的 HTML 片段。"""

    def test_contains_scene_id(self) -> None:
        scene = {"start": 0.0, "duration": 10.0}
        html = gen_scene_html(0, scene, "测试标题", "测试段落。")
        assert 'id="scene-1"' in html

    def test_contains_title(self) -> None:
        scene = {"start": 5.0, "duration": 8.0}
        html = gen_scene_html(1, scene, "我的标题", "一些内容。")
        assert "我的标题" in html

    def test_contains_data_attributes(self) -> None:
        scene = {"start": 3.5, "duration": 12.0}
        html = gen_scene_html(0, scene, "标题", "段落。")
        assert 'data-start="3.50"' in html
        assert 'data-duration="12.00"' in html

    def test_items_from_sentences(self) -> None:
        scene = {"start": 0.0, "duration": 10.0}
        html = gen_scene_html(0, scene, "标题", "第一句。第二句。第三句。")
        assert "第一句" in html
        assert "第二句" in html

    def test_max_four_items(self) -> None:
        scene = {"start": 0.0, "duration": 10.0}
        para = "句一。句二。句三。句四。句五。句六。"
        html = gen_scene_html(0, scene, "标题", para)
        assert "句五" not in html
