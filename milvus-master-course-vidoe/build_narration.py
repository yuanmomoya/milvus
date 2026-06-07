"""按段落拆分 narration.txt，逐段调用豆包 TTS，拼接成完整 narration.mp3 并输出时长 JSON。"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from doubao_tts import TTSConfig, synthesize


def get_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", str(path)],
        capture_output=True, text=True,
    )
    return float(json.loads(result.stdout)["format"]["duration"])


def build_narration(chapter_dir: Path) -> dict:
    txt = (chapter_dir / "narration.txt").read_text(encoding="utf-8")
    paragraphs = [p.strip() for p in txt.split("\n\n") if p.strip()]

    tmp_dir = Path(tempfile.mkdtemp(prefix="tts_"))
    config = TTSConfig()
    scene_files: list[Path] = []
    scenes: list[dict] = []
    offset = 0.0

    for i, para in enumerate(paragraphs):
        out_path = tmp_dir / f"scene_{i:02d}.mp3"
        synthesize(para, out_path, config)
        dur = get_duration(out_path)
        scenes.append({"index": i, "start": round(offset, 2), "duration": round(dur, 2), "chars": len(para)})
        offset += dur
        scene_files.append(out_path)

    list_file = tmp_dir / "concat.txt"
    list_file.write_text("\n".join(f"file '{f}'" for f in scene_files), encoding="utf-8")

    output_mp3 = chapter_dir / "narration.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file), "-c:a", "libmp3lame", "-b:a", "160k", str(output_mp3)],
        capture_output=True, check=True,
    )

    total_dur = get_duration(output_mp3)
    timing = {"total_duration": round(total_dur, 2), "scenes": scenes}

    timing_path = chapter_dir / "narration_timing.json"
    timing_path.write_text(json.dumps(timing, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Done: {output_mp3} ({total_dur:.1f}s, {len(scenes)} scenes)")
    return timing


if __name__ == "__main__":
    base = Path(__file__).parent
    for ch_dir in sorted(base.glob("chapter-*")):
        if (ch_dir / "narration.txt").exists():
            print(f"\n=== {ch_dir.name} ===")
            build_narration(ch_dir)
