"""Remap GSAP timeline and scene data-start/duration based on new TTS timing."""
from __future__ import annotations

import json
import re
from pathlib import Path


def remap_chapter(chapter_dir: Path, old_scenes: list[dict], new_scenes: list[dict]):
    """
    old_scenes / new_scenes: list of {start, duration} dicts, one per scene.
    Reads index.html, updates data-duration, data-start on scenes, and rescales GSAP times.
    """
    html_path = chapter_dir / "index.html"
    html = html_path.read_text(encoding="utf-8")

    total_new = new_scenes[-1]["start"] + new_scenes[-1]["duration"]

    # Update composition data-duration
    html = re.sub(r'(data-duration=")[\d.]+(")', rf'\g<1>{total_new:.1f}\2', html, count=1)
    # Update audio data-duration
    html = re.sub(r'(id="narration"[^>]*data-duration=")[\d.]+(")', rf'\g<1>{total_new:.1f}\2', html)

    # Update each scene's data-start and data-duration
    for i, ns in enumerate(new_scenes):
        scene_id = f"scene-{i+1}"
        pattern = rf'(id="{scene_id}"[^>]*data-start=")[\d.]+(\"[^>]*data-duration=\")([\d.]+)(\")'
        replacement = rf'\g<1>{ns["start"]:.1f}\g<2>{ns["duration"]:.1f}\4'
        html = re.sub(pattern, replacement, html)

    # Remap GSAP absolute times
    def map_time(t: float) -> float:
        for idx, old in enumerate(old_scenes):
            old_end = old["start"] + old["duration"]
            if t < old_end or idx == len(old_scenes) - 1:
                ratio = (t - old["start"]) / old["duration"] if old["duration"] > 0 else 0
                ratio = max(0, min(1, ratio))
                return new_scenes[idx]["start"] + ratio * new_scenes[idx]["duration"]
        return t

    # Find all numeric time arguments in tl.fromTo / tl.to calls (last numeric arg on line)
    def replace_gsap_time(match):
        time_str = match.group(1)
        try:
            old_t = float(time_str)
            new_t = map_time(old_t)
            return f", {new_t:.1f})"
        except ValueError:
            return match.group(0)

    # Match patterns like: }, 12.5); or }, 0.3);
    html = re.sub(r',\s*([\d.]+)\);', replace_gsap_time, html)

    # Also handle the pattern: }, value) at end of tl calls (without semicolon on same match)
    # The above regex should catch most. Let's also handle }, XX.X) patterns
    html = re.sub(r',\s*([\d.]+)\)(?=;)', replace_gsap_time, html)

    html_path.write_text(html, encoding="utf-8")
    print(f"Updated {html_path} (total duration: {total_new:.1f}s)")


def main():
    base = Path(__file__).parent

    # Chapter 01
    ch01 = base / "chapter-01-vector-database-basics"
    old_ch01 = [
        {"start": 0, "duration": 11.5},
        {"start": 11.5, "duration": 12.8},
        {"start": 24.3, "duration": 17.7},
        {"start": 42, "duration": 16.3},
        {"start": 58.3, "duration": 12.6},
        {"start": 70.9, "duration": 18},
        {"start": 88.9, "duration": 14},
        {"start": 102.9, "duration": 13.8},
        {"start": 116.7, "duration": 23},
        {"start": 139.7, "duration": 13.3},
    ]
    with open(ch01 / "narration_timing.json", encoding="utf-8") as f:
        timing = json.load(f)
    new_ch01 = [{"start": s["start"], "duration": s["duration"]} for s in timing["scenes"]]
    remap_chapter(ch01, old_ch01, new_ch01)

    # Chapter 02
    ch02 = base / "chapter-02-milvus-architecture"
    old_ch02 = [
        {"start": 0, "duration": 15.4},
        {"start": 15.4, "duration": 17.4},
        {"start": 32.8, "duration": 22.4},
        {"start": 55.2, "duration": 25.4},
        {"start": 80.6, "duration": 17.6},
        {"start": 98.2, "duration": 25.4},
        {"start": 123.6, "duration": 23.8},
        {"start": 147.4, "duration": 12.6},
    ]
    with open(ch02 / "narration_timing.json", encoding="utf-8") as f:
        timing = json.load(f)
    new_ch02 = [{"start": s["start"], "duration": s["duration"]} for s in timing["scenes"]]
    remap_chapter(ch02, old_ch02, new_ch02)


if __name__ == "__main__":
    main()
