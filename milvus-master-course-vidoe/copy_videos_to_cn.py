"""按教程文档的中文名将视频复制到 videos/ 并生成同名简介 txt。"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path("/Users/changmeng.yuan.o/Desktop/milvus")
DOCS_DIR = ROOT / "milvus-master-course" / "docs"
VIDEO_SRC = ROOT / "milvus-master-course-vidoe"
DEST = ROOT / "videos"

DEST.mkdir(exist_ok=True)

# 章节号 -> 中文文件名（不含 .md）
chapter_names: dict[str, str] = {}
for md in sorted(DOCS_DIR.glob("*.md")):
    m = re.match(r"^(\d{2})-(.+)\.md$", md.name)
    if m:
        chapter_names[m.group(1)] = m.group(2)

# 章节号 -> 视频源目录
chapter_dirs: dict[str, Path] = {}
for d in sorted(VIDEO_SRC.glob("chapter-*")):
    if not d.is_dir():
        continue
    m = re.match(r"^chapter-(\d{2})-", d.name)
    if m:
        chapter_dirs[m.group(1)] = d


def make_intro(num: str, cn_name: str, narration: str) -> str:
    """从旁白生成简介：取首段（hook + 前置说明）。"""
    paragraphs = [p.strip() for p in narration.split("\n\n") if p.strip()]
    intro = paragraphs[0] if paragraphs else ""
    return f"第 {num} 章 · {cn_name}\n\n{intro}\n"


for num, cn_name in chapter_names.items():
    src_dir = chapter_dirs.get(num)
    if not src_dir:
        print(f"[SKIP {num}] 找不到对应章节目录")
        continue

    src_mp4 = src_dir / f"chapter-{num}.mp4"
    src_txt = src_dir / "narration.txt"
    if not src_mp4.exists():
        print(f"[SKIP {num}] 视频缺失：{src_mp4.name}")
        continue

    dest_mp4 = DEST / f"{num}-{cn_name}.mp4"
    dest_txt = DEST / f"{num}-{cn_name}.txt"

    shutil.copy2(src_mp4, dest_mp4)

    narration = src_txt.read_text(encoding="utf-8") if src_txt.exists() else ""
    dest_txt.write_text(make_intro(num, cn_name, narration), encoding="utf-8")

    print(f"[OK {num}] {dest_mp4.name}")

print(f"\n完成。输出目录：{DEST}")
