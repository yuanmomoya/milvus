"""Generate chapter-03 index.html with subtitle layer from narration timing."""
from __future__ import annotations

import json
import re
from pathlib import Path

CH_DIR = Path(__file__).parent / "chapter-03-quick-start"
TIMING = json.loads((CH_DIR / "narration_timing.json").read_text())
NARRATION = (CH_DIR / "narration.txt").read_text()

TOTAL = TIMING["total_duration"]
SCENES = TIMING["scenes"]
PARAGRAPHS = [p.strip() for p in NARRATION.split("\n\n") if p.strip()]


def split_sentences(text: str) -> list[str]:
    parts = re.split(r'(?<=[。！？])', text)
    return [p.strip() for p in parts if p.strip()]


def gen_subtitles() -> tuple[str, str]:
    """Return (subtitle HTML elements, GSAP animation code)."""
    html_parts = []
    gsap_parts = []
    sub_idx = 0

    for scene_idx, scene in enumerate(SCENES):
        para = PARAGRAPHS[scene_idx]
        sentences = split_sentences(para)
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
            html_parts.append(f'    <div class="subtitle-text" id="{sub_id}">{sent}</div>')
            gsap_parts.append(f'  tl.fromTo("#{sub_id}", {{opacity:0}}, {{opacity:1, duration:0.25, ease:"power2.out"}}, {start_t:.1f});')
            gsap_parts.append(f'  tl.to("#{sub_id}", {{opacity:0, duration:0.25, ease:"power2.in"}}, {end_t - 0.3:.1f});')

            offset += dur
            sub_idx += 1

    return "\n".join(html_parts), "\n".join(gsap_parts)


# Scene visual content descriptions for the HTML
SCENE_VISUALS = [
    # Scene 1: Hook
    ('hook', '五步跑通 Milvus', ['启动服务', '连接', '建表', '写入', '搜索']),
    # Scene 2: Docker
    ('docker', 'Docker Compose 启动', ['docker compose up -d', 'curl healthz → OK', '三个服务就绪']),
    # Scene 3: Connect
    ('connect', 'MilvusClient 连接', ['MilvusClient(uri="...")', 'list_collections()', '返回 [] → 成功']),
    # Scene 4: Collection
    ('collection', '创建 Collection', ['Schema: id + text + embedding', 'Index: HNSW + COSINE', 'create → load → 就绪']),
    # Scene 5: Embedding
    ('embedding', '生成 Embedding', ['bge-small-zh-v1.5', '文本 → 512 维向量', 'model.encode(texts)']),
    # Scene 6: Write
    ('write', 'upsert 写入', ['upsert(data)', '幂等：相同 PK 覆盖', '写入 WAL → 立即可查']),
    # Scene 7: Search
    ('search', '语义搜索', ['query → encode → vector', 'search(TopK)', '铁律：同一个模型']),
    # Scene 8: Summary
    ('summary', '五步闭环', ['启动 → 连接 → 建表 → 写入 → 搜索', 'RAG / 图片 / 多模态', '核心流程不变']),
]


def gen_scene_html(idx: int, scene: dict, visual: tuple) -> str:
    tag, title, items = visual
    s_id = idx + 1
    start = scene["start"]
    dur = scene["duration"]

    items_html = "\n".join(
        f'        <div class="item-row" id="s{s_id}-item{i+1}"><span class="item-bullet">▸</span> {item}</div>'
        for i, item in enumerate(items)
    )

    return f'''  <!-- Scene {s_id}: {title} ({start:.1f}s - {start+dur:.1f}s) -->
  <div id="scene-{s_id}" class="scene clip" data-start="{start:.1f}" data-duration="{dur:.1f}" data-track-index="{s_id}">
    <div class="scene-bg">
      <div class="glow glow-{s_id}a"></div>
      <div class="glow glow-{s_id}b"></div>
      <div class="particle p{(idx%7)+1}"></div>
      <div class="particle p{((idx+3)%7)+1}"></div>
    </div>
    <div class="scene-content">
      <div class="section-title" id="s{s_id}-title">{title}</div>
      <div class="item-list">
{items_html}
      </div>
    </div>
  </div>
'''


def gen_gsap_scenes() -> str:
    lines = []
    for idx, scene in enumerate(SCENES):
        s_id = idx + 1
        start = scene["start"]
        _, _, items = SCENE_VISUALS[idx]

        lines.append(f"  // === Scene {s_id} ({start:.1f}s) ===")
        lines.append(f'  tl.fromTo("#s{s_id}-title", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.5, ease:"expo.out"}}, {start + 0.5:.1f});')
        for i in range(len(items)):
            t = start + 1.5 + i * 1.8
            lines.append(f'  tl.fromTo("#s{s_id}-item{i+1}", {{opacity:0, x:-30}}, {{opacity:1, x:0, duration:0.4, ease:"power3.out"}}, {t:.1f});')
        lines.append("")
    return "\n".join(lines)


def main():
    subtitle_html, subtitle_gsap = gen_subtitles()
    scenes_html = "\n".join(gen_scene_html(i, s, SCENE_VISUALS[i]) for i, s in enumerate(SCENES))
    scenes_gsap = gen_gsap_scenes()

    html = f'''<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>03 Milvus 快速开始</title>
</head>
<body>
<div data-composition-id="ch03-quick-start" data-start="0" data-duration="{TOTAL:.1f}" data-width="1920" data-height="1080">

  <audio id="narration" data-start="0" data-duration="{TOTAL:.1f}" data-track-index="0" src="narration.mp3" data-volume="1"></audio>

{scenes_html}
  <!-- Subtitle Layer -->
  <div id="subtitle-bar" class="subtitle-layer clip" data-start="0" data-duration="{TOTAL:.1f}" data-track-index="99">
    <div class="subtitle-bg"></div>
{subtitle_html}
  </div>

</div>

<style>
[data-composition-id="ch03-quick-start"] {{
  position: relative; width: 1920px; height: 1080px; overflow: hidden;
  background: #0f1729; font-family: "Noto Sans SC", sans-serif; color: #e8edf5;
}}
.scene {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; }}
.scene-bg {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; }}
.scene-content {{
  position: relative; display: flex; flex-direction: column; justify-content: center;
  width: 100%; height: 100%; padding: 100px 140px 160px; gap: 28px; box-sizing: border-box; z-index: 2;
}}

/* Glows */
.glow {{ position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.15; }}
.glow-1a {{ width: 600px; height: 600px; background: #00d4aa; top: -100px; right: -100px; }}
.glow-1b {{ width: 400px; height: 400px; background: #a78bfa; bottom: -50px; left: 10%; }}
.glow-2a {{ width: 500px; height: 500px; background: #f59e0b; top: -100px; left: -50px; }}
.glow-2b {{ width: 350px; height: 350px; background: #00d4aa; bottom: -80px; right: 20%; }}
.glow-3a {{ width: 500px; height: 500px; background: #a78bfa; top: 50%; left: -100px; transform: translateY(-50%); }}
.glow-3b {{ width: 300px; height: 300px; background: #00d4aa; top: -80px; right: 15%; }}
.glow-4a {{ width: 600px; height: 500px; background: #00d4aa; bottom: -100px; right: -50px; }}
.glow-4b {{ width: 350px; height: 350px; background: #a78bfa; top: -80px; left: 20%; }}
.glow-5a {{ width: 500px; height: 500px; background: #f59e0b; top: -100px; right: 20%; }}
.glow-5b {{ width: 400px; height: 400px; background: #a78bfa; bottom: -100px; left: -50px; }}
.glow-6a {{ width: 500px; height: 500px; background: #00d4aa; bottom: -100px; left: 30%; }}
.glow-6b {{ width: 300px; height: 300px; background: #f59e0b; top: -80px; right: 10%; }}
.glow-7a {{ width: 600px; height: 500px; background: #a78bfa; top: -100px; left: -50px; }}
.glow-7b {{ width: 350px; height: 350px; background: #00d4aa; bottom: -80px; right: 20%; }}
.glow-8a {{ width: 700px; height: 600px; background: #a78bfa; top: 50%; left: 50%; transform: translate(-50%, -50%); opacity: 0.18; }}
.glow-8b {{ width: 300px; height: 300px; background: #00d4aa; top: -80px; left: 20%; }}

/* Particles */
.particle {{
  position: absolute; width: 6px; height: 6px; border-radius: 50%; background: #00d4aa; opacity: 0.3;
  animation: drift 20s infinite ease-in-out;
}}
.p1 {{ top: 15%; left: 10%; animation-delay: 0s; }}
.p2 {{ top: 70%; left: 85%; animation-delay: -4s; background: #a78bfa; }}
.p3 {{ top: 40%; left: 60%; animation-delay: -8s; width: 4px; height: 4px; }}
.p4 {{ top: 80%; left: 25%; animation-delay: -2s; background: #f59e0b; }}
.p5 {{ top: 20%; left: 75%; animation-delay: -6s; width: 8px; height: 8px; opacity: 0.2; }}
.p6 {{ top: 55%; left: 15%; animation-delay: -10s; background: #a78bfa; width: 5px; height: 5px; }}
.p7 {{ top: 30%; left: 90%; animation-delay: -14s; }}
@keyframes drift {{
  0%, 100% {{ transform: translate(0, 0); }}
  25% {{ transform: translate(30px, -20px); }}
  50% {{ transform: translate(-15px, 25px); }}
  75% {{ transform: translate(20px, 10px); }}
}}

/* Scene content */
.section-title {{ font-size: 64px; font-weight: 800; }}
.item-list {{ display: flex; flex-direction: column; gap: 18px; margin-top: 16px; }}
.item-row {{
  display: flex; align-items: center; gap: 16px; font-size: 36px;
  background: #1a2744; padding: 20px 32px; border-radius: 10px;
  font-family: "JetBrains Mono", monospace; color: #8b9dc3;
}}
.item-bullet {{ color: #00d4aa; font-size: 28px; }}

/* Subtitle Layer */
.subtitle-layer {{
  position: absolute; bottom: 0; left: 0; width: 100%; height: 100px;
  z-index: 100;
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

  // Ambient glow breathing
  tl.to(".glow-1a", {{ scale: 1.1, opacity: 0.22, duration: 3.5, yoyo: true, repeat: 50, ease: "sine.inOut" }}, 0);

{scenes_gsap}
  // === Subtitles ===
{subtitle_gsap}

  window.__timelines["ch03-quick-start"] = tl;
}})();
</script>

</div>
</body>
</html>
'''

    output = CH_DIR / "index.html"
    output.write_text(html, encoding="utf-8")
    print(f"Generated {output} ({len(html)} bytes, {TOTAL:.1f}s)")


if __name__ == "__main__":
    main()
