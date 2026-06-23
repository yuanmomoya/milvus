"""逐章生成 TTS、分镜 HTML 和 HyperFrames 视频，并保存可恢复的进度。"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from build_narration import build_narration
from storyboard_html import generate_html, validate_workspace


BASE = Path(__file__).resolve().parent
PROGRESS_PATH = BASE / "batch_video_progress.json"


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load_progress() -> dict:
    if PROGRESS_PATH.exists():
        return json.loads(PROGRESS_PATH.read_text(encoding="utf-8"))
    return {"started_at": now(), "chapters": {}}


def save_progress(progress: dict) -> None:
    progress["updated_at"] = now()
    PROGRESS_PATH.write_text(
        json.dumps(progress, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def chapter_number(chapter_dir: Path) -> str:
    return chapter_dir.name.split("-")[1]


def output_video(chapter_dir: Path) -> Path:
    return chapter_dir / f"chapter-{chapter_number(chapter_dir)}.mp4"


def audio_ready(chapter_dir: Path) -> bool:
    return (
        (chapter_dir / "narration.mp3").exists()
        and (chapter_dir / "narration.mp3").stat().st_size > 100_000
        and (chapter_dir / "narration_timing.json").exists()
    )


def video_ready(chapter_dir: Path) -> bool:
    path = output_video(chapter_dir)
    return path.exists() and path.stat().st_size > 1_000_000


def update(progress: dict, chapter_dir: Path, phase: str, status: str, **details: object) -> None:
    chapter = progress["chapters"].setdefault(chapter_dir.name, {})
    chapter[phase] = {"status": status, "at": now(), **details}
    save_progress(progress)
    print(
        f"[{datetime.now().strftime('%H:%M:%S')}] "
        f"{chapter_dir.name} {phase}: {status}",
        flush=True,
    )


def render_video(chapter_dir: Path) -> None:
    number = chapter_number(chapter_dir)
    command = (
        "source ~/.nvm/nvm.sh && "
        "nvm use 22 >/dev/null && "
        f"npx --yes --registry=https://registry.npmjs.org hyperframes render "
        f"--output chapter-{number}.mp4"
    )
    log_path = chapter_dir / "render.log"
    with log_path.open("w", encoding="utf-8") as log_file:
        result = subprocess.run(
            ["zsh", "-lc", command],
            cwd=chapter_dir,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            text=True,
        )
    if result.returncode != 0:
        tail = "\n".join(log_path.read_text(encoding="utf-8").splitlines()[-30:])
        raise RuntimeError(f"HyperFrames 渲染失败，日志末尾：\n{tail}")


def process_audio(chapter_dir: Path, progress: dict, force: bool) -> None:
    if audio_ready(chapter_dir) and not force:
        update(progress, chapter_dir, "audio", "skipped")
        return
    update(progress, chapter_dir, "audio", "running")
    started = time.monotonic()
    timing = build_narration(chapter_dir)
    generate_html(chapter_dir)
    validate_workspace(chapter_dir)
    update(
        progress,
        chapter_dir,
        "audio",
        "completed",
        elapsed_seconds=round(time.monotonic() - started, 1),
        duration=timing["total_duration"],
        scenes=len(timing["scenes"]),
    )


def process_render(chapter_dir: Path, progress: dict, force: bool) -> None:
    video = output_video(chapter_dir)
    if video_ready(chapter_dir) and not force:
        validate_workspace(chapter_dir, video)
        update(progress, chapter_dir, "render", "validated")
        return
    if not audio_ready(chapter_dir):
        raise RuntimeError(f"{chapter_dir.name} 缺少有效 narration.mp3")
    generate_html(chapter_dir)
    update(progress, chapter_dir, "render", "running")
    started = time.monotonic()
    render_video(chapter_dir)
    validate_workspace(chapter_dir, video)
    update(
        progress,
        chapter_dir,
        "render",
        "completed",
        elapsed_seconds=round(time.monotonic() - started, 1),
        bytes=video.stat().st_size,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="批量生成 Milvus 课程视频")
    parser.add_argument(
        "--phase",
        choices=("audio", "render", "all"),
        default="all",
        help="执行音频、视频或完整流水线",
    )
    parser.add_argument("--from-chapter", default="00", help="从指定两位章节号开始")
    parser.add_argument("--to-chapter", default="40", help="执行到指定两位章节号结束")
    parser.add_argument("--force", action="store_true", help="覆盖已经有效的产物")
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="单章失败后继续执行其余章节",
    )
    args = parser.parse_args()

    if args.phase in {"audio", "all"} and not os.getenv("DOUBAO_TTS_API_KEY"):
        raise RuntimeError("缺少 DOUBAO_TTS_API_KEY，无法生成 TTS")

    chapters = [
        path
        for path in sorted(BASE.glob("chapter-*"))
        if path.is_dir()
        and args.from_chapter <= chapter_number(path) <= args.to_chapter
    ]
    progress = load_progress()
    progress["command"] = {
        "phase": args.phase,
        "from_chapter": args.from_chapter,
        "to_chapter": args.to_chapter,
        "force": args.force,
    }
    save_progress(progress)

    failures: list[str] = []
    for chapter_dir in chapters:
        try:
            if args.phase in {"audio", "all"}:
                process_audio(chapter_dir, progress, args.force)
            if args.phase in {"render", "all"}:
                process_render(chapter_dir, progress, args.force)
        except Exception as exc:  # noqa: BLE001 - 需要把单章错误记录后决定是否继续
            failures.append(chapter_dir.name)
            update(progress, chapter_dir, args.phase, "failed", error=str(exc))
            if not args.continue_on_error:
                raise

    progress["finished_at"] = now()
    progress["failures"] = failures
    save_progress(progress)
    print(
        f"Batch complete: chapters={len(chapters)}, failures={len(failures)}",
        flush=True,
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
