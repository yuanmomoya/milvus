"""storyboard_html.py 单元测试：文本处理与 beat 映射。"""
from __future__ import annotations

from storyboard_html import beat_slot, scene_points, split_sentences


class TestSplitSentences:
    """split_sentences 应按中文句末标点拆分。"""

    def test_basic_split(self) -> None:
        assert split_sentences("你好。世界！") == ["你好。", "世界！"]

    def test_empty(self) -> None:
        assert split_sentences("") == []

    def test_strips(self) -> None:
        result = split_sentences("  句子一。 句子二。 ")
        assert result == ["句子一。", "句子二。"]


class TestScenePoints:
    """scene_points 应从 Scene dict 提取要点列表。"""

    def test_key_points_present(self) -> None:
        scene = {"key_points": ["要点一", "要点二", "要点三"], "title": "标题"}
        result = scene_points(scene)
        assert result == ["要点一", "要点二", "要点三"]

    def test_pads_with_components(self) -> None:
        scene = {"key_points": ["要点一"], "components": ["comp-a", "comp-b", "comp-c"], "title": "标题"}
        result = scene_points(scene, minimum=3)
        assert len(result) >= 3
        assert "comp a" in result[1] or "comp b" in result[1]

    def test_empty_key_points_uses_title(self) -> None:
        scene = {"key_points": [], "title": "标题内容"}
        result = scene_points(scene)
        assert result == ["标题内容"]

    def test_no_key_points_key(self) -> None:
        scene = {"title": "默认标题"}
        result = scene_points(scene)
        assert result == ["默认标题"]

    def test_filters_empty_strings(self) -> None:
        scene = {"key_points": ["", "有效内容", "  "], "title": "标题"}
        result = scene_points(scene, minimum=1)
        assert "" not in result

    def test_default_minimum_three(self) -> None:
        scene = {"key_points": ["仅一个"], "components": ["c1", "c2", "c3"]}
        result = scene_points(scene)
        assert len(result) >= 3


class TestBeatSlot:
    """beat_slot 应将 index 限制在 Scene 实际 beat 数量之内。"""

    def test_within_range(self) -> None:
        scene = {"beats": [{"at": 0.0}, {"at": 0.36}, {"at": 0.72}]}
        assert beat_slot(scene, 1) == 1
        assert beat_slot(scene, 2) == 2
        assert beat_slot(scene, 3) == 3

    def test_index_exceeds_beats(self) -> None:
        scene = {"beats": [{"at": 0.0}, {"at": 0.5}]}
        assert beat_slot(scene, 5) == 2

    def test_empty_beats(self) -> None:
        scene = {"beats": []}
        assert beat_slot(scene, 3) == 1

    def test_no_beats_key(self) -> None:
        scene = {}
        assert beat_slot(scene, 3) == 1

    def test_index_zero(self) -> None:
        scene = {"beats": [{"at": 0.0}, {"at": 0.5}]}
        assert beat_slot(scene, 0) == 0
