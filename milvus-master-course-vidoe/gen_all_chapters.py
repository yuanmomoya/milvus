"""Universal chapter HTML generator with subtitle layer."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).parent


def split_sentences(text: str) -> list[str]:
    parts = re.split(r'(?<=[。！？])', text)
    return [p.strip() for p in parts if p.strip()]


def gen_subtitles(scenes: list[dict], paragraphs: list[str]) -> tuple[str, str]:
    html_parts = []
    gsap_parts = []
    sub_idx = 0

    for scene_idx, scene in enumerate(scenes):
        if scene_idx >= len(paragraphs):
            break
        para = paragraphs[scene_idx]
        sentences = split_sentences(para)
        if not sentences:
            sentences = [para]
        total_chars = sum(len(s) for s in sentences)
        scene_start = scene["start"]
        scene_dur = scene["duration"]

        offset = 0.0
        for sent in sentences:
            ratio = len(sent) / total_chars if total_chars > 0 else 1 / len(sentences)
            dur = scene_dur * ratio
            start_t = scene_start + offset
            end_t = start_t + dur

            sub_id = f"sub-{sub_idx:02d}"
            display_text = sent.replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
            html_parts.append(f'    <div class="subtitle-text" id="{sub_id}">{display_text}</div>')
            gsap_parts.append(f'  tl.fromTo("#{sub_id}", {{opacity:0}}, {{opacity:1, duration:0.25, ease:"power2.out"}}, {start_t:.2f});')
            gsap_parts.append(f'  tl.to("#{sub_id}", {{opacity:0, duration:0.25, ease:"power2.in"}}, {end_t - 0.3:.2f});')

            offset += dur
            sub_idx += 1

    return "\n".join(html_parts), "\n".join(gsap_parts)


def extract_title(para: str) -> str:
    """Extract a short title from the first sentence of a paragraph."""
    first_sent = split_sentences(para)
    if first_sent:
        t = first_sent[0][:20]
    else:
        t = para[:20]
    return t.rstrip("。！？，、")


def gen_scene_html(idx: int, scene: dict, title: str, para: str) -> str:
    s_id = idx + 1
    start = scene["start"]
    dur = scene["duration"]
    sentences = split_sentences(para)
    if not sentences:
        sentences = [para]
    items = sentences[:4]

    items_html = "\n".join(
        f'        <div class="item-row" id="s{s_id}-item{i+1}"><span class="item-bullet">▸</span> {item[:60]}</div>'
        for i, item in enumerate(items)
    )

    return f'''  <!-- Scene {s_id}: {title} ({start:.1f}s - {start+dur:.1f}s) -->
  <div id="scene-{s_id}" class="scene clip" data-start="{start:.2f}" data-duration="{dur:.2f}" data-track-index="{s_id}">
    <div class="scene-bg">
      <div class="glow glow-{(idx%4)+1}a"></div>
      <div class="glow glow-{(idx%4)+1}b"></div>
    </div>
    <div class="scene-content">
      <div class="section-title" id="s{s_id}-title">{title}</div>
      <div class="item-list">
{items_html}
      </div>
    </div>
  </div>
'''


def gen_gsap_scenes(scenes: list[dict], paragraphs: list[str]) -> str:
    lines = []
    for idx, scene in enumerate(scenes):
        if idx >= len(paragraphs):
            break
        s_id = idx + 1
        start = scene["start"]
        para = paragraphs[idx]
        sentences = split_sentences(para)
        if not sentences:
            sentences = [para]
        items = sentences[:4]

        lines.append(f"  // === Scene {s_id} ({start:.1f}s) ===")
        lines.append(f'  tl.fromTo("#s{s_id}-title", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.5, ease:"expo.out"}}, {start + 0.3:.2f});')
        for i in range(len(items)):
            t = start + 1.2 + i * 1.5
            if t < start + scene["duration"] - 0.5:
                lines.append(f'  tl.fromTo("#s{s_id}-item{i+1}", {{opacity:0, x:-30}}, {{opacity:1, x:0, duration:0.4, ease:"power3.out"}}, {t:.2f});')
        lines.append("")
    return "\n".join(lines)


def generate_chapter(ch_dir: Path) -> None:
    timing_path = ch_dir / "narration_timing.json"
    narration_path = ch_dir / "narration.txt"

    if not timing_path.exists() or not narration_path.exists():
        print(f"  Skipping {ch_dir.name}: missing files")
        return

    timing = json.loads(timing_path.read_text())
    narration = narration_path.read_text()

    total = timing["total_duration"]
    scenes = timing["scenes"]
    paragraphs = [p.strip() for p in narration.split("\n\n") if p.strip()]

    ch_name = ch_dir.name
    ch_num = ch_name.split("-")[0].replace("chapter", "")
    comp_id = f"ch{ch_num}-{'-'.join(ch_name.split('-')[1:4])}"
    ch_title_raw = ch_name.replace("chapter-", "").replace("-", " ").title()

    titles = [extract_title(p) for p in paragraphs]

    scenes_html = "\n".join(
        gen_scene_html(i, s, titles[i] if i < len(titles) else f"Scene {i+1}", paragraphs[i] if i < len(paragraphs) else "")
        for i, s in enumerate(scenes) if i < len(paragraphs)
    )
    scenes_gsap = gen_gsap_scenes(scenes, paragraphs)
    subtitle_html, subtitle_gsap = gen_subtitles(scenes, paragraphs)

    html = f'''<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>{ch_num} {ch_title_raw}</title>
</head>
<body>
<div data-composition-id="{comp_id}" data-start="0" data-duration="{total:.2f}" data-width="1920" data-height="1080">

  <audio id="narration" data-start="0" data-duration="{total:.2f}" data-track-index="0" src="narration.mp3" data-volume="1"></audio>

{scenes_html}
  <!-- Subtitle Layer -->
  <div id="subtitle-bar" class="subtitle-layer clip" data-start="0" data-duration="{total:.2f}" data-track-index="99">
    <div class="subtitle-bg"></div>
{subtitle_html}
  </div>

</div>

<style>
[data-composition-id="{comp_id}"] {{
  position: relative; width: 1920px; height: 1080px; overflow: hidden;
  background: #0f1729; font-family: "Noto Sans SC", "PingFang SC", sans-serif; color: #e8edf5;
}}
.scene {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; }}
.scene-bg {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; }}
.scene-content {{
  position: relative; display: flex; flex-direction: column; justify-content: center;
  width: 100%; height: 100%; padding: 100px 140px 160px; gap: 28px; box-sizing: border-box; z-index: 2;
}}

.glow {{ position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.15; }}
.glow-1a {{ width: 600px; height: 600px; background: #00d4aa; top: -100px; right: -100px; }}
.glow-1b {{ width: 400px; height: 400px; background: #a78bfa; bottom: -50px; left: 10%; }}
.glow-2a {{ width: 500px; height: 500px; background: #f59e0b; top: -100px; left: -50px; }}
.glow-2b {{ width: 350px; height: 350px; background: #00d4aa; bottom: -80px; right: 20%; }}
.glow-3a {{ width: 500px; height: 500px; background: #a78bfa; top: 50%; left: -100px; transform: translateY(-50%); }}
.glow-3b {{ width: 300px; height: 300px; background: #00d4aa; top: -80px; right: 15%; }}
.glow-4a {{ width: 600px; height: 500px; background: #00d4aa; bottom: -100px; right: -50px; }}
.glow-4b {{ width: 350px; height: 350px; background: #a78bfa; top: -80px; left: 20%; }}

.particle {{
  position: absolute; width: 6px; height: 6px; border-radius: 50%; background: #00d4aa; opacity: 0.3;
  animation: drift 20s infinite ease-in-out;
}}
@keyframes drift {{
  0%, 100% {{ transform: translate(0, 0); }}
  25% {{ transform: translate(30px, -20px); }}
  50% {{ transform: translate(-15px, 25px); }}
  75% {{ transform: translate(20px, 10px); }}
}}

.section-title {{ font-size: 56px; font-weight: 800; opacity: 0; }}
.item-list {{ display: flex; flex-direction: column; gap: 16px; margin-top: 16px; }}
.item-row {{
  display: flex; align-items: center; gap: 16px; font-size: 32px;
  background: #1a2744; padding: 18px 28px; border-radius: 10px;
  color: #8b9dc3; opacity: 0;
}}
.item-bullet {{ color: #00d4aa; font-size: 24px; }}

.subtitle-layer {{
  position: absolute; bottom: 0; left: 0; width: 100%; height: 100px; z-index: 100;
}}
.subtitle-bg {{
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(15, 23, 41, 0.85);
  border-top: 1px solid rgba(0, 212, 170, 0.3);
}}
.subtitle-text {{
  position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
  font-size: 34px; font-weight: 500; color: #e8edf5; text-align: center;
  width: 88%; opacity: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}}
</style>

<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
window.__timelines = window.__timelines || {{}};

(function() {{
  var tl = gsap.timeline({{ paused: true }});

  tl.to(".glow-1a", {{ scale: 1.08, opacity: 0.2, duration: 4, yoyo: true, repeat: 50, ease: "sine.inOut" }}, 0);

{scenes_gsap}
  // === Subtitles ===
{subtitle_gsap}

  window.__timelines["{comp_id}"] = tl;
}})();
</script>

</div>
</body>
</html>
'''

    output = ch_dir / "index.html"
    output.write_text(html, encoding="utf-8")
    print(f"  Generated {output.name} ({len(html)} bytes, {total:.1f}s, {len(scenes)} scenes)")


def main():
    chapters = sorted(BASE.glob("chapter-*"))
    print(f"Generating HTML for {len(chapters)} chapters...\n")
    for ch_dir in chapters:
        if ch_dir.is_dir():
            print(f"=== {ch_dir.name} ===")
            generate_chapter(ch_dir)
    print("\nDone!")


if __name__ == "__main__":
    main()
