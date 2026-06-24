"""校验所有章节 storyboard.md 与旁白、timing 的一致性。"""
from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path

BASE = Path(__file__).parent
ALLOWED_VISUAL_TYPES = {
    "hook-comparison",
    "learning-map",
    "pipeline",
    "vector-space",
    "metric-comparison",
    "graph-search",
    "cluster-search",
    "compression",
    "code-terminal",
    "architecture",
    "dashboard",
    "error-diagnosis",
    "recap",
}


def parse_storyboard(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    blocks = re.findall(r"```toml\n(.*?)\n```", text, re.S)
    if len(blocks) != 1:
        raise ValueError(f"应包含且只包含一个 TOML 代码块，实际为 {len(blocks)}")
    return tomllib.loads(blocks[0])


def validate_chapter(chapter_dir: Path) -> list[str]:
    errors: list[str] = []
    storyboard_path = chapter_dir / "storyboard.md"
    if not storyboard_path.exists():
        return ["缺少 storyboard.md"]
    try:
        storyboard = parse_storyboard(storyboard_path)
    except (ValueError, tomllib.TOMLDecodeError) as exc:
        return [f"storyboard 解析失败: {exc}"]

    narration_path = chapter_dir / "narration.txt"
    timing_path = chapter_dir / "narration_timing.json"
    if not narration_path.exists():
        errors.append("缺少 narration.txt")
        return errors
    if not timing_path.exists():
        errors.append("缺少 narration_timing.json")
        return errors
    narration = narration_path.read_text(encoding="utf-8")
    paragraphs = [part.strip() for part in narration.split("\n\n") if part.strip()]
    try:
        timing = json.loads(timing_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"narration_timing.json 不是有效 JSON: {exc}")
        return errors
    scenes = storyboard.get("scenes", [])
    expected_chapter = chapter_dir.name.split("-", 2)[1]

    if storyboard.get("schema_version") != 1:
        errors.append("schema_version 必须为 1")
    if storyboard.get("chapter") != expected_chapter:
        errors.append(
            f"chapter={storyboard.get('chapter')}，目录章节号={expected_chapter}"
        )
    if storyboard.get("renderer") != "hyperframes":
        errors.append("renderer 必须为 hyperframes")
    if storyboard.get("motion_canvas") is not False:
        errors.append("motion_canvas 当前必须为 false")
    if not (chapter_dir / storyboard.get("narration_file", "")).exists():
        errors.append("narration_file 不存在")
    if not (chapter_dir / storyboard.get("timing_file", "")).exists():
        errors.append("timing_file 不存在")

    source_doc = storyboard.get("source_doc")
    if not source_doc or not (chapter_dir / source_doc).resolve().exists():
        errors.append(f"source_doc 不存在: {source_doc}")

    if not (len(scenes) == len(paragraphs) == len(timing.get("scenes", []))):
        errors.append(
            f"Scene 数不一致: storyboard={len(scenes)}, "
            f"narration={len(paragraphs)}, timing={len(timing.get('scenes', []))}"
        )

    indexes = [scene.get("narration_index") for scene in scenes]
    if indexes != list(range(1, len(scenes) + 1)):
        errors.append("narration_index 必须从 1 连续递增")

    ids = [scene.get("id") for scene in scenes]
    if len(ids) != len(set(ids)):
        errors.append("Scene id 重复")

    for scene in scenes:
        scene_id = scene.get("id", "<unknown>")
        if scene.get("visual_type") not in ALLOWED_VISUAL_TYPES:
            errors.append(f"{scene_id}: 非法 visual_type={scene.get('visual_type')}")
        if not scene.get("key_points"):
            errors.append(f"{scene_id}: key_points 不能为空")
        if not scene.get("components"):
            errors.append(f"{scene_id}: components 不能为空")
        beats = scene.get("beats", [])
        if len(beats) < 3:
            errors.append(f"{scene_id}: 至少需要 3 个 Beat")
            continue
        values = [beat.get("at") for beat in beats]
        if any(not isinstance(value, (int, float)) for value in values):
            errors.append(f"{scene_id}: Beat at 必须为数字")
            continue
        if values != sorted(values) or len(values) != len(set(values)):
            errors.append(f"{scene_id}: Beat at 必须严格递增")
        if any(value < 0 or value > 1 for value in values):
            errors.append(f"{scene_id}: Beat at 必须处于 0.0-1.0")

    return errors


def main() -> None:
    failed = 0
    chapters = [path for path in sorted(BASE.glob("chapter-*")) if path.is_dir()]
    for chapter_dir in chapters:
        errors = validate_chapter(chapter_dir)
        if errors:
            failed += 1
            print(f"FAIL {chapter_dir.name}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK   {chapter_dir.name}")
    print(f"\nValidated {len(chapters)} chapters, failed={failed}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
