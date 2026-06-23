"""根据 storyboard.md、旁白和 timing 生成分镜驱动的 HyperFrames HTML。"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import tomllib
from pathlib import Path


STORYBOARD_BLOCK = re.compile(r"```toml\s*(.*?)```", re.DOTALL)


def split_sentences(text: str) -> list[str]:
    """按中文句末标点拆分字幕。"""
    parts = re.split(r"(?<=[。！？])", text)
    return [part.strip() for part in parts if part.strip()]


def read_storyboard(path: Path) -> dict:
    """读取 storyboard.md 中的 TOML 数据块。"""
    match = STORYBOARD_BLOCK.search(path.read_text(encoding="utf-8"))
    if not match:
        raise ValueError(f"{path} 中没有 TOML 分镜数据块")
    return tomllib.loads(match.group(1))


def prepare_workspace(source_dir: Path, output_dir: Path) -> None:
    """把章节内容源复制到独立输出目录，不覆盖正式章节产物。"""
    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_dir / "narration.txt", output_dir / "narration.txt")

    storyboard_path = source_dir / "storyboard.md"
    storyboard_text = storyboard_path.read_text(encoding="utf-8")
    storyboard = read_storyboard(storyboard_path)
    source_doc = storyboard.get("source_doc")
    if source_doc:
        resolved_doc = (source_dir / source_doc).resolve()
        adjusted = Path(os.path.relpath(resolved_doc, output_dir.resolve())).as_posix()
        storyboard_text = re.sub(
            r'^source_doc\s*=\s*"[^"]+"',
            f'source_doc = "{adjusted}"',
            storyboard_text,
            count=1,
            flags=re.MULTILINE,
        )
    (output_dir / "storyboard.md").write_text(storyboard_text, encoding="utf-8")
    print(f"Prepared: {output_dir}")


def car_icon(css_class: str) -> str:
    return f"""
      <svg class="{css_class}" viewBox="0 0 180 90" aria-hidden="true">
        <path d="M25 61h130l-10-30-34-15H66L43 34z" fill="currentColor" opacity=".95"/>
        <rect x="10" y="50" width="160" height="25" rx="10" fill="currentColor"/>
        <circle cx="48" cy="76" r="13" fill="#0b1224" stroke="currentColor" stroke-width="6"/>
        <circle cx="135" cy="76" r="13" fill="#0b1224" stroke="currentColor" stroke-width="6"/>
        <path d="M70 25h36l23 19H56z" fill="#0f1729" opacity=".72"/>
      </svg>
    """


def truck_icon(css_class: str) -> str:
    return f"""
      <svg class="{css_class}" viewBox="0 0 210 100" aria-hidden="true">
        <rect x="12" y="15" width="125" height="60" rx="8" fill="currentColor"/>
        <path d="M137 36h38l25 25v14h-63z" fill="currentColor" opacity=".9"/>
        <path d="M151 43h21l16 17h-37z" fill="#0f1729" opacity=".72"/>
        <circle cx="52" cy="79" r="14" fill="#0b1224" stroke="currentColor" stroke-width="7"/>
        <circle cx="163" cy="79" r="14" fill="#0b1224" stroke="currentColor" stroke-width="7"/>
      </svg>
    """


def render_hook(scene_no: int) -> str:
    if scene_no == 1:
        return f"""
        <div class="question-card anim beat-1">
          <span class="eyebrow">语义相似性问题</span>
          <strong>轿车和香蕉，哪个更像卡车？</strong>
        </div>
        <div class="vehicle-stage anim beat-2">
          <div class="vehicle sedan">{car_icon("vehicle-svg")}<span>轿车</span></div>
          <div class="similarity-line strong"><i></i><b>语义更近</b></div>
          <div class="vehicle truck">{truck_icon("vehicle-svg")}<span>卡车</span></div>
          <div class="similarity-line weak"><i></i><b>语义很远</b></div>
          <div class="vehicle banana">
            <svg class="banana-svg" viewBox="0 0 150 110" aria-hidden="true">
              <path d="M24 24c12 58 56 76 104 46-15 36-55 48-88 27C15 81 7 48 15 24z"
                    fill="currentColor"/>
              <path d="M21 22l-8-9" stroke="currentColor" stroke-width="7" stroke-linecap="round"/>
            </svg>
            <span>香蕉</span>
          </div>
        </div>
        <div class="db-compare anim beat-3">
          <div class="db-card traditional"><span>传统数据库</span><b>字段条件无法直接表达“像”</b></div>
          <div class="db-arrow">→</div>
          <div class="db-card vector"><span>向量数据库</span><b>根据语义表示计算相似度</b></div>
        </div>
        <div class="learning-path anim beat-4">
          <span>01 向量表示</span><i></i><span>02 距离度量</span><i></i><span>03 索引加速</span>
        </div>
        """

    return """
      <div class="compare-board">
        <div class="compare-panel old anim beat-1">
          <span class="panel-tag">传统数据库</span>
          <div class="shelf">
            <i data-code="A-017"></i><i data-code="A-018"></i><i data-code="B-204"></i>
            <i data-code="C-031"></i><i data-code="C-032"></i><i data-code="D-110"></i>
          </div>
          <div class="search-pill">精确编号：B-204</div>
          <b>按字段与编号定位</b>
        </div>
        <div class="versus anim beat-2">VS</div>
        <div class="compare-panel new anim beat-3">
          <span class="panel-tag">向量数据库</span>
          <div class="semantic-map">
            <i class="dot d1"></i><i class="dot d2"></i><i class="dot d3"></i>
            <i class="dot d4"></i><i class="dot d5"></i><i class="dot query"></i>
            <svg viewBox="0 0 420 230"><path d="M230 108C285 64 324 77 359 45M230 108C288 124 323 150 366 172"
              fill="none" stroke="#00d4aa" stroke-width="4" stroke-dasharray="10 9"/></svg>
          </div>
          <div class="search-pill accent">寻找语义邻居 TopK</div>
          <b>意思相近，自然靠近</b>
        </div>
      </div>
    """


def render_pipeline() -> str:
    return """
      <div class="pipeline-stage">
        <div class="source-stack anim beat-1">
          <div class="source-card">“Milvus 向量检索”</div>
          <div class="source-card image-card"><span></span><i></i><b></b></div>
        </div>
        <div class="flow-arrow anim beat-1"><i></i></div>
        <div class="embedding-machine anim beat-2">
          <span>Embedding</span><strong>坐标测量仪</strong>
          <div class="machine-grid"></div>
        </div>
        <div class="flow-arrow anim beat-2"><i></i></div>
        <div class="vector-output anim beat-3">
          <span>384 维向量</span>
          <code>[0.12, -0.03, 0.88, …]</code>
        </div>
        <div class="vector-plane anim beat-4">
          <span class="axis x">语义维度 X</span><span class="axis y">语义维度 Y</span>
          <i class="point p1"></i><i class="point p2"></i><i class="point p3"></i>
          <i class="point p4"></i><i class="point p5"></i><i class="point p6"></i>
          <div class="cluster-label vehicle-label">交通工具</div>
          <div class="cluster-label fruit-label">水果</div>
        </div>
      </div>
    """


def render_metrics() -> str:
    return """
      <div class="metric-grid">
        <div class="metric-card anim beat-1">
          <span class="metric-name">COSINE</span><strong>看方向</strong>
          <svg viewBox="0 0 300 170">
            <path d="M55 135L236 55M55 135L251 105" stroke="#00d4aa" stroke-width="7"
                  stroke-linecap="round"/>
            <path d="M113 110A64 64 0 0 1 119 97" fill="none" stroke="#f59e0b" stroke-width="5"/>
            <text x="125" y="110" fill="#f59e0b" font-size="24">夹角</text>
          </svg>
          <em>方向越接近，相似度越高</em>
        </div>
        <div class="metric-card anim beat-2">
          <span class="metric-name">L2</span><strong>看直线距离</strong>
          <svg viewBox="0 0 300 170">
            <circle cx="65" cy="115" r="12" fill="#a78bfa"/><circle cx="235" cy="58" r="12" fill="#00d4aa"/>
            <path d="M77 111L222 63" stroke="#e8edf5" stroke-width="5" stroke-dasharray="11 8"/>
            <text x="125" y="72" fill="#e8edf5" font-size="24">distance</text>
          </svg>
          <em>距离越小，向量越接近</em>
        </div>
        <div class="metric-card anim beat-3">
          <span class="metric-name">IP</span><strong>方向 × 长度</strong>
          <svg viewBox="0 0 300 170">
            <path d="M55 135L250 55M55 135L191 79" stroke="#a78bfa" stroke-width="7"
                  stroke-linecap="round"/>
            <circle cx="55" cy="135" r="9" fill="#f59e0b"/>
            <text x="98" y="147" fill="#8b9dc3" font-size="22">内积得分</text>
          </svg>
          <em>同向且更长，得分通常更高</em>
        </div>
      </div>
      <div class="metric-rule anim beat-4"><span>同一个任务中</span><strong>Embedding、索引和查询必须使用一致的度量方式</strong></div>
    """


def render_scale_dashboard() -> str:
    dots = "".join("<i></i>" for _ in range(72))
    return f"""
      <div class="scale-layout">
        <div class="scale-copy">
          <div class="scale-number anim beat-1"><span>向量数量</span><strong>100</strong></div>
          <div class="scale-number danger anim beat-2"><span>规模上升</span><strong>100,000,000</strong></div>
          <div class="complexity anim beat-3"><span>FLAT 全量扫描</span><b>一次查询 ≈ 一亿次距离计算</b></div>
          <div class="ann-answer anim beat-4"><span>ANN 的目标</span><b>先缩小候选集，再精细比较</b></div>
        </div>
        <div class="scan-visual anim beat-1">
          <div class="dot-grid">{dots}</div>
          <div class="scan-beam"></div>
          <div class="latency-gauge"><span>计算成本</span><i></i></div>
          <div class="candidate-window anim beat-4">候选集</div>
        </div>
      </div>
    """


def render_hnsw() -> str:
    return """
      <div class="hnsw-board">
        <div class="layer layer-top anim beat-1"><span>L2 高速层</span>
          <i style="left:12%"></i><i style="left:48%"></i><i style="left:83%"></i>
          <b style="left:14%;width:68%"></b>
        </div>
        <div class="layer layer-mid anim beat-2"><span>L1 中间层</span>
          <i style="left:7%"></i><i style="left:25%"></i><i style="left:48%"></i>
          <i style="left:67%"></i><i style="left:88%"></i>
          <b style="left:9%;width:77%"></b>
        </div>
        <div class="layer layer-base anim beat-3"><span>L0 邻接图</span>
          <i style="left:3%"></i><i style="left:14%"></i><i style="left:25%"></i><i style="left:36%"></i>
          <i style="left:47%"></i><i style="left:58%"></i><i style="left:69%"></i><i style="left:80%"></i>
          <i class="target" style="left:91%"></i><b style="left:5%;width:84%"></b>
        </div>
        <svg class="search-route anim beat-4" viewBox="0 0 1200 560">
          <path d="M145 75L613 75L1025 75L825 270L1054 270L965 467L1100 467"
                fill="none" stroke="#f59e0b" stroke-width="10" stroke-linecap="round"
                stroke-linejoin="round" stroke-dasharray="18 13"/>
        </svg>
        <div class="route-label anim beat-4">长跳转 → 逐层下沉 → 局部精搜</div>
      </div>
    """


def render_ivf() -> str:
    clusters = []
    positions = [
        ("c1", 18, 33), ("c1", 24, 23), ("c1", 29, 41), ("c1", 34, 29),
        ("c2", 57, 26), ("c2", 64, 18), ("c2", 68, 36), ("c2", 74, 27),
        ("c3", 28, 72), ("c3", 37, 64), ("c3", 42, 79), ("c3", 48, 69),
        ("c4", 70, 69), ("c4", 77, 60), ("c4", 82, 78), ("c4", 88, 68),
    ]
    for cls, left, top in positions:
        clusters.append(f'<i class="cluster-dot {cls}" style="left:{left}%;top:{top}%"></i>')
    return f"""
      <div class="ivf-board anim beat-1">
        <div class="cluster-zone z1"></div><div class="cluster-zone z2 selected"></div>
        <div class="cluster-zone z3"></div><div class="cluster-zone z4 selected"></div>
        {''.join(clusters)}
        <b class="centroid ct1">C1</b><b class="centroid ct2">C2</b>
        <b class="centroid ct3">C3</b><b class="centroid ct4">C4</b>
        <div class="query-point anim beat-2">Q</div>
        <svg class="probe-lines anim beat-3" viewBox="0 0 1200 610">
          <path d="M590 310L755 165M590 310L925 430" stroke="#00d4aa" stroke-width="7"
                stroke-dasharray="14 12"/>
        </svg>
        <div class="ivf-stats anim beat-4"><span><b>nlist = 4</b> 建库时分四簇</span><span><b>nprobe = 2</b> 查询时只搜两簇</span></div>
      </div>
    """


def render_compression() -> str:
    original = "".join(f"<i>{value}</i>" for value in ["0.12", "-0.03", "0.88", "0.41", "-0.26", "0.67", "0.09", "-0.51"])
    encoded = "".join(f"<b>{value}</b>" for value in ["17", "03", "28", "11"])
    return f"""
      <div class="pq-board">
        <div class="long-vector anim beat-1"><span>原始 Float32 向量</span><div>{original}<em>…</em></div></div>
        <div class="slice-guide anim beat-2"><i></i><i></i><i></i><i></i><span>切成 m 个子向量</span></div>
        <div class="codebook-row anim beat-3">
          <div class="codebook"><span>码本 1</span><i></i><i></i><i></i></div>
          <div class="codebook"><span>码本 2</span><i></i><i></i><i></i></div>
          <div class="codebook"><span>码本 3</span><i></i><i></i><i></i></div>
          <div class="codebook"><span>码本 4</span><i></i><i></i><i></i></div>
        </div>
        <div class="short-code anim beat-3"><span>短编码</span><div>{encoded}</div></div>
        <div class="memory-compare anim beat-4">
          <div><span>原始向量</span><i class="bar full"></i></div>
          <div><span>PQ 编码</span><i class="bar compact"></i></div>
          <b>内存显著下降</b><em>召回率可能有损，需用真实数据评测</em>
        </div>
      </div>
    """


def render_kpi_dashboard() -> str:
    return """
      <div class="kpi-grid">
        <div class="kpi-card recall anim beat-1"><span>Recall</span><strong>召回率</strong><div class="ring">95<small>%</small></div><em>该找到的找到了多少</em></div>
        <div class="kpi-card qps anim beat-2"><span>QPS</span><strong>吞吐量</strong><div class="bars"><i></i><i></i><i></i><i></i><i></i></div><em>每秒处理多少请求</em></div>
        <div class="kpi-card latency anim beat-3"><span>Latency</span><strong>查询延迟</strong><svg viewBox="0 0 330 115"><path d="M5 93C55 88 65 55 108 68S172 76 199 38S261 83 325 17" fill="none" stroke="#f59e0b" stroke-width="6"/></svg><em>重点观察 P95 / P99</em></div>
        <div class="kpi-card memory anim beat-4"><span>Memory</span><strong>资源成本</strong><div class="memory-stack"><i></i><i></i><i></i><i></i></div><em>容量与预算是否平衡</em></div>
      </div>
      <div class="tradeoff anim beat-5"><span>调高搜索强度</span><i></i><strong>召回 ↑</strong><b>延迟与资源成本也可能 ↑</b></div>
    """


def render_recap() -> str:
    return """
      <div class="recap-board">
        <div class="recap-flow anim beat-1">
          <div><span>01</span><strong>Embedding</strong><em>把内容变成向量</em></div><i></i>
          <div><span>02</span><strong>Metric</strong><em>定义什么叫相似</em></div><i></i>
          <div><span>03</span><strong>ANN Index</strong><em>在海量数据中加速</em></div>
        </div>
        <div class="tool-row anim beat-2">
          <span>HNSW<br><b>图搜索</b></span><span>IVF<br><b>聚类缩小范围</b></span>
          <span>PQ<br><b>压缩向量</b></span><span>四项指标<br><b>寻找平衡点</b></span>
        </div>
        <div class="next-card anim beat-3">
          <span>下一章</span><strong>Milvus 如何把这套组合拳工程化？</strong>
          <div class="milvus-mark"><i></i><i></i><i></i></div>
        </div>
      </div>
    """


def scene_points(scene: dict, minimum: int = 3) -> list[str]:
    points = [str(point) for point in scene.get("key_points", []) if str(point).strip()]
    components = [
        str(component).replace("-", " ").replace("_", " ")
        for component in scene.get("components", [])
        if str(component).strip()
    ]
    for component in components:
        if len(points) >= minimum:
            break
        points.append(component)
    return points or [scene.get("title", "本节核心内容")]


def beat_slot(scene: dict, index: int) -> int:
    """把视觉元素映射到该 Scene 实际存在的 Beat，避免元素永久透明。"""
    return min(index, max(1, len(scene.get("beats", []))))


def render_generic_cards(scene: dict, css_class: str = "generic-board") -> str:
    points = "".join(
        f'<div class="generic-point anim beat-{beat_slot(scene, index)}"><span>{index:02d}</span>'
        f'<b>{html.escape(point)}</b></div>'
        for index, point in enumerate(scene_points(scene), start=1)
    )
    return f'<div class="{css_class}">{points}</div>'


def render_generic_comparison(scene: dict) -> str:
    points = scene_points(scene)
    left = html.escape(points[0])
    right = html.escape(points[1] if len(points) > 1 else scene["title"])
    takeaway = html.escape(points[2] if len(points) > 2 else "根据场景选择合适方案")
    return f"""
      <div class="story-comparison">
        <div class="story-side warm anim beat-{beat_slot(scene, 1)}"><span>方案 A</span><strong>{left}</strong><i></i></div>
        <div class="story-vs anim beat-{beat_slot(scene, 2)}">VS</div>
        <div class="story-side cool anim beat-{beat_slot(scene, 3)}"><span>方案 B</span><strong>{right}</strong><i></i></div>
        <div class="story-takeaway anim beat-{beat_slot(scene, 4)}"><span>关键结论</span><b>{takeaway}</b></div>
      </div>
    """


def render_generic_pipeline(scene: dict) -> str:
    points = scene_points(scene)
    steps = []
    for index, point in enumerate(points[:5], start=1):
        steps.append(
            f'<div class="story-step anim beat-{beat_slot(scene, index)}"><span>{index:02d}</span>'
            f'<strong>{html.escape(point)}</strong></div>'
        )
    return '<div class="story-pipeline">' + '<i class="story-flow"></i>'.join(steps) + "</div>"


def render_generic_vector_space(scene: dict) -> str:
    points = scene_points(scene)
    labels = [
        html.escape(points[index] if index < len(points) else f"语义区域 {index + 1}")
        for index in range(3)
    ]
    dots = "".join(
        f'<i class="space-dot group-{group}" style="left:{left}%;top:{top}%"></i>'
        for group, left, top in [
            (1, 18, 27), (1, 25, 36), (1, 30, 22), (1, 34, 42),
            (2, 60, 20), (2, 68, 30), (2, 75, 18), (2, 80, 35),
            (3, 43, 68), (3, 50, 76), (3, 57, 63), (3, 62, 78),
        ]
    )
    return f"""
      <div class="story-space anim beat-{beat_slot(scene, 1)}">
        {dots}
        <div class="space-label l1">{labels[0]}</div>
        <div class="space-label l2">{labels[1]}</div>
        <div class="space-label l3">{labels[2]}</div>
        <div class="space-query anim beat-{beat_slot(scene, 2)}">Q</div>
        <svg class="space-links anim beat-{beat_slot(scene, 3)}" viewBox="0 0 1200 600">
          <path d="M580 300L320 210M580 300L785 170M580 300L635 430"
                fill="none" stroke="#00d4aa" stroke-width="6" stroke-dasharray="13 10"/>
        </svg>
      </div>
    """


def render_generic_graph(scene: dict) -> str:
    points = scene_points(scene)
    nodes = []
    positions = [(15, 46), (34, 20), (51, 47), (70, 20), (86, 49)]
    for index, (left, top) in enumerate(positions):
        label = html.escape(points[index % len(points)])
        nodes.append(
            f'<div class="story-node anim beat-{beat_slot(scene, index + 1)}" '
            f'style="left:{left}%;top:{top}%"><span>{index + 1:02d}</span><b>{label}</b></div>'
        )
    return f"""
      <div class="story-graph">
        <svg viewBox="0 0 1200 600">
          <path d="M210 330L430 180L610 330L835 180L1035 335"
                fill="none" stroke="#4b5d82" stroke-width="8"/>
          <path d="M210 330L610 330L1035 335"
                fill="none" stroke="#00d4aa" stroke-width="7" stroke-dasharray="16 12"/>
        </svg>
        {''.join(nodes)}
      </div>
    """


def render_generic_clusters(scene: dict) -> str:
    points = scene_points(scene)
    clusters = []
    for index, (left, top, color) in enumerate(
        [(8, 20, "teal"), (38, 12, "violet"), (22, 58, "warm"), (62, 50, "teal")]
    ):
        label = html.escape(points[index % len(points)])
        clusters.append(
            f'<div class="story-cluster {color} anim beat-{beat_slot(scene, index + 1)}" '
            f'style="left:{left}%;top:{top}%"><i></i><i></i><i></i><i></i>'
            f'<strong>{label}</strong></div>'
        )
    return f'<div class="story-clusters">{"".join(clusters)}<div class="cluster-query">Q</div></div>'


def render_generic_compression(scene: dict) -> str:
    points = scene_points(scene)
    before = html.escape(points[0])
    process = html.escape(points[1] if len(points) > 1 else "编码与压缩")
    after = html.escape(points[2] if len(points) > 2 else "降低资源占用")
    return f"""
      <div class="story-compression">
        <div class="compression-box before anim beat-{beat_slot(scene, 1)}"><span>BEFORE</span><strong>{before}</strong>
          <div class="data-bars">{'<i></i>' * 8}</div></div>
        <div class="compression-process anim beat-{beat_slot(scene, 2)}"><b>{process}</b><i>→</i></div>
        <div class="compression-box after anim beat-{beat_slot(scene, 3)}"><span>AFTER</span><strong>{after}</strong>
          <div class="data-bars compact">{'<i></i>' * 4}</div></div>
      </div>
    """


def render_generic_terminal(scene: dict) -> str:
    lines = []
    for index, point in enumerate(scene_points(scene)[:6], start=1):
        lines.append(
            f'<div class="terminal-line anim beat-{beat_slot(scene, index)}"><span>{index:02d}</span>'
            f'<code>{html.escape(point)}</code></div>'
        )
    return f"""
      <div class="story-terminal">
        <header><i></i><i></i><i></i><span>milvus-course — chapter demo</span></header>
        <main>{''.join(lines)}</main>
        <footer><b>✓</b> 流程与参数来自本章 storyboard</footer>
      </div>
    """


def render_generic_architecture(scene: dict) -> str:
    points = scene_points(scene)
    blocks = []
    for index, point in enumerate(points[:6], start=1):
        blocks.append(
            f'<div class="arch-block anim beat-{beat_slot(scene, index)}"><span>{index:02d}</span>'
            f'<strong>{html.escape(point)}</strong></div>'
        )
    return f"""
      <div class="story-architecture">
        <div class="arch-client">请求 / 数据</div>
        <i class="arch-arrow">↓</i>
        <div class="arch-grid">{''.join(blocks)}</div>
        <i class="arch-arrow">↓</i>
        <div class="arch-storage">存储、计算与治理共同完成本章目标</div>
      </div>
    """


def render_generic_dashboard(scene: dict) -> str:
    points = scene_points(scene)
    cards = []
    colors = ["#00d4aa", "#a78bfa", "#f59e0b", "#ef4444", "#38bdf8"]
    for index, point in enumerate(points[:5], start=1):
        cards.append(
            f'<div class="story-kpi anim beat-{beat_slot(scene, index)}" style="--accent:{colors[(index - 1) % len(colors)]}">'
            f'<span>0{index}</span><strong>{html.escape(point)}</strong>'
            f'<div><i style="height:{30 + index * 9}%"></i><i style="height:{55 + index * 5}%"></i>'
            f'<i style="height:{42 + index * 8}%"></i><i style="height:{70 + index * 4}%"></i></div></div>'
        )
    return f'<div class="story-dashboard">{"".join(cards)}</div>'


def render_generic_diagnosis(scene: dict) -> str:
    points = scene_points(scene)
    labels = [
        html.escape(points[index] if index < len(points) else fallback)
        for index, fallback in enumerate(["观察现象", "定位原因", "执行修复"])
    ]
    return f"""
      <div class="story-diagnosis">
        <div class="diagnosis-step symptom anim beat-{beat_slot(scene, 1)}"><span>现象</span><strong>{labels[0]}</strong></div>
        <i>→</i>
        <div class="diagnosis-step cause anim beat-{beat_slot(scene, 2)}"><span>原因</span><strong>{labels[1]}</strong></div>
        <i>→</i>
        <div class="diagnosis-step fix anim beat-{beat_slot(scene, 3)}"><span>处理</span><strong>{labels[2]}</strong></div>
      </div>
    """


def render_generic_recap(scene: dict) -> str:
    points = scene_points(scene)
    items = "".join(
        f'<div class="recap-item anim beat-{beat_slot(scene, index)}"><span>{index:02d}</span>'
        f'<strong>{html.escape(point)}</strong></div>'
        for index, point in enumerate(points[:5], start=1)
    )
    return f"""
      <div class="story-recap">
        <div class="recap-orbit"><div class="recap-core">{html.escape(scene["title"])}</div>{items}</div>
      </div>
    """


def render_generic_visual(scene: dict) -> str:
    visual_type = scene.get("visual_type")
    if visual_type == "hook-comparison":
        return render_generic_comparison(scene)
    if visual_type in {"learning-map", "pipeline"}:
        return render_generic_pipeline(scene)
    if visual_type == "vector-space":
        return render_generic_vector_space(scene)
    if visual_type == "metric-comparison":
        return render_generic_cards(scene, "generic-board metric-generic")
    if visual_type == "graph-search":
        return render_generic_graph(scene)
    if visual_type == "cluster-search":
        return render_generic_clusters(scene)
    if visual_type == "compression":
        return render_generic_compression(scene)
    if visual_type == "code-terminal":
        return render_generic_terminal(scene)
    if visual_type == "architecture":
        return render_generic_architecture(scene)
    if visual_type == "dashboard":
        return render_generic_dashboard(scene)
    if visual_type == "error-diagnosis":
        return render_generic_diagnosis(scene)
    if visual_type == "recap":
        return render_generic_recap(scene)
    return render_generic_cards(scene)


def render_visual(chapter: str, scene_no: int, scene: dict) -> str:
    if chapter != "01":
        return render_generic_visual(scene)
    visual_type = scene.get("visual_type")
    if visual_type == "hook-comparison":
        return render_hook(scene_no)
    if visual_type == "pipeline":
        return render_pipeline()
    if visual_type == "metric-comparison":
        return render_metrics()
    if visual_type == "dashboard" and scene_no == 5:
        return render_scale_dashboard()
    if visual_type == "graph-search":
        return render_hnsw()
    if visual_type == "cluster-search":
        return render_ivf()
    if visual_type == "compression":
        return render_compression()
    if visual_type == "dashboard":
        return render_kpi_dashboard()
    if visual_type == "recap":
        return render_recap()
    return render_generic(scene)


def render_scene(chapter: str, scene_no: int, scene: dict, timing: dict, duration: float) -> str:
    title = html.escape(scene["title"])
    purpose = html.escape(scene.get("purpose", "concept").upper())
    key_points = "".join(f"<span>{html.escape(point)}</span>" for point in scene.get("key_points", []))
    return f"""
  <section id="scene-{scene_no}" class="scene clip scene-{scene_no}" data-start="{timing['start']:.2f}"
           data-duration="{duration:.2f}" data-track-index="{scene_no}">
    <div class="ambient"><i></i><i></i><i></i></div>
    <header class="scene-header">
      <div><span class="scene-number">{scene_no:02d}</span><span class="purpose">{purpose}</span></div>
      <h2>{title}</h2>
    </header>
    <div class="visual-shell">{render_visual(chapter, scene_no, scene)}</div>
    <div class="key-point-strip">{key_points}</div>
  </section>
    """


def render_subtitles(timing_scenes: list[dict], paragraphs: list[str]) -> tuple[str, str]:
    html_parts: list[str] = []
    timeline_parts: list[str] = []
    subtitle_no = 0
    for scene, paragraph in zip(timing_scenes, paragraphs, strict=True):
        sentences = split_sentences(paragraph) or [paragraph]
        total_chars = sum(len(sentence) for sentence in sentences)
        offset = 0.0
        for sentence in sentences:
            duration = scene["duration"] * len(sentence) / total_chars
            start = scene["start"] + offset
            end = start + duration
            subtitle_id = f"subtitle-{subtitle_no:02d}"
            html_parts.append(f'<div id="{subtitle_id}" class="subtitle-text">{html.escape(sentence)}</div>')
            fade_out = max(start + 0.35, end - 0.22)
            timeline_parts.append(
                f'tl.fromTo("#{subtitle_id}", {{opacity:0,y:10}}, '
                f'{{opacity:1,y:0,duration:.18,ease:"power2.out"}}, {start:.2f});'
            )
            timeline_parts.append(
                f'tl.to("#{subtitle_id}", {{opacity:0,y:-8,duration:.16,ease:"power2.in"}}, {fade_out:.2f});'
            )
            subtitle_no += 1
            offset += duration
    return "\n".join(html_parts), "\n".join(timeline_parts)


CSS = r"""
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#0b1224}
[data-composition-id]{position:relative;overflow:hidden;background:#0f1729;color:#e8edf5;
font-family:"Noto Sans SC","PingFang SC","Microsoft YaHei",sans-serif}
.scene{position:absolute;inset:0;padding:55px 88px 150px;overflow:hidden;background:#0f1729}
.scene:before{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(139,157,195,.045) 1px,transparent 1px),
linear-gradient(90deg,rgba(139,157,195,.045) 1px,transparent 1px);background-size:64px 64px}
.ambient i{position:absolute;border-radius:50%;filter:blur(90px);opacity:.14}
.ambient i:nth-child(1){width:530px;height:530px;background:#00d4aa;right:-120px;top:-180px}
.ambient i:nth-child(2){width:440px;height:440px;background:#a78bfa;left:-160px;bottom:-120px}
.ambient i:nth-child(3){width:260px;height:260px;background:#f59e0b;left:48%;top:32%;opacity:.07}
.scene-header{position:relative;z-index:2;display:flex;align-items:flex-end;justify-content:space-between;height:115px;
border-bottom:1px solid rgba(139,157,195,.22);padding-bottom:22px}
.scene-header>div{display:flex;gap:14px;align-items:center}
.scene-number{font:800 30px/1 "JetBrains Mono",monospace;color:#00d4aa}
.purpose{font:700 18px/1 "JetBrains Mono",monospace;letter-spacing:.16em;color:#8b9dc3;border:1px solid rgba(139,157,195,.3);
padding:9px 13px;border-radius:99px}
.scene-header h2{margin:0;font-size:52px;line-height:1.1;font-weight:850;letter-spacing:-.025em;text-align:right}
.visual-shell{position:relative;z-index:2;height:700px;margin-top:20px}
.key-point-strip{position:absolute;z-index:3;left:88px;right:88px;bottom:118px;display:flex;gap:10px}
.key-point-strip span{font-size:20px;color:#8b9dc3;background:rgba(26,39,68,.85);border:1px solid rgba(139,157,195,.16);
padding:10px 16px;border-radius:8px}
.anim{opacity:0}
.question-card{position:absolute;left:0;top:30px;width:620px;padding:31px 36px;background:#1a2744;border:1px solid rgba(0,212,170,.35);
border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,.24)}
.question-card .eyebrow{display:block;color:#00d4aa;font-size:20px;font-weight:700;letter-spacing:.08em;margin-bottom:13px}
.question-card strong{font-size:40px;line-height:1.35}
.vehicle-stage{position:absolute;left:700px;right:0;top:22px;height:360px}
.vehicle{position:absolute;width:220px;height:170px;display:flex;flex-direction:column;align-items:center;justify-content:center;
background:#151f37;border:1px solid rgba(139,157,195,.18);border-radius:22px;color:#8b9dc3}
.vehicle span{font-size:25px;font-weight:800;margin-top:8px}.vehicle-svg{width:150px;color:#00d4aa}.sedan{left:0;top:0}.truck{right:0;top:0}
.truck .vehicle-svg{width:165px;color:#00d4aa}.banana{left:50%;bottom:0;transform:translateX(-50%);height:145px}
.banana-svg{width:108px;color:#f59e0b}.similarity-line{position:absolute;top:76px;height:58px}
.similarity-line i{position:absolute;left:0;right:0;top:12px;border-top:5px dashed #00d4aa}
.similarity-line b{position:absolute;top:28px;left:50%;transform:translateX(-50%);white-space:nowrap;color:#00d4aa;font-size:20px}
.similarity-line.strong{left:205px;right:205px}.similarity-line.weak{left:305px;right:85px;top:210px;transform:rotate(-18deg)}
.similarity-line.weak i{border-color:#8b9dc3;opacity:.4}.similarity-line.weak b{color:#8b9dc3;transform:translateX(-50%) rotate(18deg)}
.db-compare{position:absolute;left:0;top:270px;width:620px;display:grid;grid-template-columns:1fr 50px 1fr;align-items:center}
.db-card{height:142px;padding:22px;border-radius:16px;background:#151f37;border:1px solid rgba(139,157,195,.18)}
.db-card span{font-size:19px;color:#8b9dc3}.db-card b{display:block;font-size:24px;line-height:1.35;margin-top:12px}
.db-card.traditional{border-color:rgba(245,158,11,.35)}.db-card.vector{border-color:rgba(0,212,170,.35)}.db-arrow{text-align:center;font-size:32px;color:#8b9dc3}
.learning-path{position:absolute;left:0;right:0;bottom:20px;height:74px;display:flex;align-items:center;justify-content:center;gap:24px;
background:rgba(21,31,55,.9);border:1px solid rgba(167,139,250,.3);border-radius:16px}
.learning-path span{font-size:25px;font-weight:750}.learning-path i{width:80px;border-top:3px solid #a78bfa;position:relative}.learning-path i:after{content:"";position:absolute;right:-2px;top:-7px;border-left:10px solid #a78bfa;border-top:6px solid transparent;border-bottom:6px solid transparent}
.compare-board{height:100%;display:grid;grid-template-columns:1fr 100px 1fr;gap:24px;align-items:center}
.compare-panel{height:550px;background:#151f37;border:1px solid rgba(139,157,195,.18);border-radius:24px;padding:30px;position:relative}
.compare-panel.old{border-color:rgba(245,158,11,.28)}.compare-panel.new{border-color:rgba(0,212,170,.28)}
.panel-tag{font-size:22px;font-weight:800;color:#8b9dc3}.compare-panel b{display:block;text-align:center;font-size:27px;margin-top:21px}
.versus{font:900 32px/1 "JetBrains Mono",monospace;color:#8b9dc3;text-align:center}
.shelf{height:300px;margin-top:32px;padding:22px;display:grid;grid-template-columns:repeat(3,1fr);gap:18px;border:12px solid #263655;border-top-width:18px}
.shelf i{position:relative;background:#a78bfa;border-radius:5px 5px 2px 2px}.shelf i:nth-child(2n){background:#f59e0b}
.shelf i:after{content:attr(data-code);position:absolute;left:50%;bottom:12px;transform:translateX(-50%) rotate(-90deg);font:700 15px monospace;color:#0f1729}
.search-pill{margin:18px auto 0;width:max-content;padding:12px 21px;border-radius:99px;background:rgba(245,158,11,.13);color:#f59e0b;font-size:20px}
.search-pill.accent{background:rgba(0,212,170,.12);color:#00d4aa}.semantic-map{height:300px;position:relative;margin-top:25px;border-radius:18px;background:radial-gradient(circle at center,rgba(0,212,170,.08),transparent 60%)}
.semantic-map svg{position:absolute;inset:0;width:100%;height:100%}.dot{position:absolute;width:34px;height:34px;border-radius:50%;background:#a78bfa;box-shadow:0 0 24px rgba(167,139,250,.35)}
.dot.d1{left:20%;top:23%}.dot.d2{left:29%;top:38%}.dot.d3{left:23%;top:61%}.dot.d4{right:14%;top:21%;background:#00d4aa}.dot.d5{right:10%;bottom:20%;background:#00d4aa}.dot.query{left:49%;top:41%;background:#f59e0b;border:6px solid #fff;width:45px;height:45px}
.pipeline-stage{height:100%;display:flex;align-items:center;gap:27px}.source-stack{width:245px;display:flex;flex-direction:column;gap:18px}
.source-card{height:110px;background:#1a2744;border:1px solid rgba(139,157,195,.2);border-radius:15px;padding:23px;font-size:24px;font-weight:700}
.image-card{position:relative;overflow:hidden}.image-card span{position:absolute;inset:18px;background:#263655;border-radius:9px}.image-card i{position:absolute;width:38px;height:38px;border-radius:50%;background:#f59e0b;right:40px;top:30px}.image-card b{position:absolute;left:30px;right:30px;bottom:24px;height:45px;background:#00d4aa;clip-path:polygon(0 100%,25% 35%,45% 70%,70% 10%,100% 100%)}
.flow-arrow{width:75px;height:4px;background:#00d4aa;position:relative}.flow-arrow i{position:absolute;right:-2px;top:-8px;border-left:16px solid #00d4aa;border-top:10px solid transparent;border-bottom:10px solid transparent}
.embedding-machine{width:260px;height:255px;border:2px solid rgba(0,212,170,.5);border-radius:28px;background:#131f38;padding:35px 28px;text-align:center;box-shadow:0 0 55px rgba(0,212,170,.12)}
.embedding-machine span{display:block;font:800 27px monospace;color:#00d4aa}.embedding-machine strong{display:block;font-size:29px;margin-top:12px}
.machine-grid{height:86px;margin-top:25px;background-image:linear-gradient(#263655 2px,transparent 2px),linear-gradient(90deg,#263655 2px,transparent 2px);background-size:22px 22px}
.vector-output{width:280px;padding:25px;background:#1a2744;border-radius:18px;border:1px solid rgba(167,139,250,.35)}
.vector-output span{display:block;color:#a78bfa;font-size:20px;font-weight:700;margin-bottom:14px}.vector-output code{font-size:24px;color:#e8edf5}
.vector-plane{position:relative;flex:1;height:500px;border-left:3px solid #8b9dc3;border-bottom:3px solid #8b9dc3;background:radial-gradient(circle at 35% 60%,rgba(0,212,170,.1),transparent 28%),radial-gradient(circle at 75% 30%,rgba(245,158,11,.1),transparent 30%)}
.axis{position:absolute;color:#8b9dc3;font-size:17px}.axis.x{right:10px;bottom:8px}.axis.y{left:8px;top:10px}.point{position:absolute;width:27px;height:27px;border-radius:50%;background:#00d4aa;box-shadow:0 0 18px rgba(0,212,170,.45)}
.point.p1{left:20%;top:58%}.point.p2{left:29%;top:68%}.point.p3{left:35%;top:52%}.point.p4{left:67%;top:22%;background:#f59e0b}.point.p5{left:75%;top:33%;background:#f59e0b}.point.p6{left:82%;top:18%;background:#f59e0b}
.cluster-label{position:absolute;font-weight:800;font-size:19px}.vehicle-label{left:20%;top:78%;color:#00d4aa}.fruit-label{right:10%;top:44%;color:#f59e0b}
.metric-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:25px;padding-top:25px}.metric-card{height:500px;padding:28px;background:#151f37;border:1px solid rgba(139,157,195,.2);border-radius:22px}
.metric-card:nth-child(1){border-top:5px solid #00d4aa}.metric-card:nth-child(2){border-top:5px solid #a78bfa}.metric-card:nth-child(3){border-top:5px solid #f59e0b}
.metric-name{font:800 21px monospace;color:#8b9dc3}.metric-card strong{display:block;font-size:34px;margin-top:14px}.metric-card svg{width:100%;height:245px;margin-top:18px}
.metric-card em{display:block;font-style:normal;color:#8b9dc3;font-size:22px;text-align:center}.metric-rule{height:92px;margin-top:24px;padding:22px 28px;border-radius:15px;background:#1a2744;display:flex;align-items:center;gap:25px}
.metric-rule span{color:#8b9dc3;font-size:21px}.metric-rule strong{font-size:25px;color:#00d4aa}
.scale-layout{height:100%;display:grid;grid-template-columns:650px 1fr;gap:60px;align-items:center}.scale-copy{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.scale-number,.complexity,.ann-answer{height:150px;padding:24px;background:#151f37;border:1px solid rgba(139,157,195,.18);border-radius:18px}
.scale-number span,.complexity span,.ann-answer span{font-size:20px;color:#8b9dc3}.scale-number strong{display:block;font:900 46px monospace;color:#00d4aa;margin-top:17px}
.scale-number.danger strong{color:#ef4444;font-size:38px}.complexity,.ann-answer{grid-column:span 2}.complexity b,.ann-answer b{display:block;font-size:29px;margin-top:16px}.complexity{border-color:rgba(239,68,68,.3)}.ann-answer{border-color:rgba(0,212,170,.3)}.ann-answer b{color:#00d4aa}
.scan-visual{height:560px;position:relative;padding:40px;background:#111b31;border-radius:24px;border:1px solid rgba(139,157,195,.18)}.dot-grid{display:grid;grid-template-columns:repeat(9,1fr);gap:22px}
.dot-grid i{width:20px;height:20px;border-radius:50%;background:#a78bfa;opacity:.65}.scan-beam{position:absolute;left:20px;top:25px;width:12px;height:450px;background:#00d4aa;filter:blur(3px);box-shadow:0 0 35px #00d4aa;animation:scan 3s ease-in-out infinite alternate}
@keyframes scan{to{left:88%}}.latency-gauge{position:absolute;left:40px;right:40px;bottom:32px;display:flex;align-items:center;gap:18px;color:#8b9dc3}.latency-gauge i{height:18px;flex:1;border-radius:99px;background:linear-gradient(90deg,#00d4aa 0 28%,#f59e0b 55%,#ef4444 100%)}
.candidate-window{position:absolute;right:88px;top:145px;width:260px;height:245px;border:5px solid #00d4aa;border-radius:22px;display:flex;align-items:flex-end;justify-content:center;padding:18px;color:#00d4aa;font-weight:800}
.hnsw-board{height:100%;position:relative;padding-top:28px}.layer{position:absolute;left:80px;right:80px;height:95px;border-radius:18px;background:#151f37;border:1px solid rgba(139,157,195,.18)}
.layer span{position:absolute;left:22px;top:16px;color:#8b9dc3;font-size:19px}.layer i{position:absolute;top:55px;width:31px;height:31px;border:7px solid #0f1729;border-radius:50%;background:#a78bfa;z-index:2}.layer b{position:absolute;top:68px;border-top:5px solid #4b5d82}
.layer-top{top:35px}.layer-mid{top:230px}.layer-base{top:425px}.layer-mid i{background:#00d4aa}.layer-base i{background:#8b9dc3}.layer-base i.target{background:#f59e0b;box-shadow:0 0 28px #f59e0b}
.search-route{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}.route-label{position:absolute;right:90px;top:335px;padding:16px 22px;border-radius:12px;background:#1a2744;color:#f59e0b;font-size:23px;font-weight:800}
.ivf-board{height:620px;position:relative;margin:10px 80px;background:#111b31;border-radius:25px;border:1px solid rgba(139,157,195,.18);overflow:hidden}
.cluster-zone{position:absolute;width:290px;height:250px;border:3px dashed rgba(139,157,195,.28);border-radius:48%}.cluster-zone.selected{border-color:#00d4aa;background:rgba(0,212,170,.05);box-shadow:0 0 45px rgba(0,212,170,.1)}
.z1{left:80px;top:35px}.z2{right:155px;top:25px}.z3{left:190px;bottom:25px}.z4{right:70px;bottom:25px}.cluster-dot{position:absolute;width:24px;height:24px;border-radius:50%;background:#8b9dc3}
.cluster-dot.c2,.cluster-dot.c4{background:#00d4aa}.centroid{position:absolute;width:54px;height:54px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#a78bfa;color:#0f1729;font:900 18px monospace}
.ct1{left:24%;top:28%}.ct2{left:64%;top:22%;background:#00d4aa}.ct3{left:35%;top:67%}.ct4{left:78%;top:66%;background:#00d4aa}
.query-point{position:absolute;left:48%;top:44%;width:66px;height:66px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#f59e0b;color:#0f1729;font:900 25px monospace;border:7px solid #fff}
.probe-lines{position:absolute;inset:0;width:100%;height:100%}.ivf-stats{position:absolute;left:30px;right:30px;bottom:16px;display:flex;justify-content:space-between}
.ivf-stats span{padding:12px 18px;background:rgba(15,23,41,.9);border-radius:10px;color:#8b9dc3;font-size:19px}.ivf-stats b{color:#00d4aa}
.pq-board{height:100%;padding:30px 40px;position:relative}.long-vector span,.short-code span{display:block;color:#8b9dc3;font-size:20px;margin-bottom:12px}.long-vector>div,.short-code>div{display:flex;gap:10px}
.long-vector i,.short-code b{font:700 21px monospace;padding:18px 14px;border-radius:9px;background:#1a2744;color:#e8edf5;font-style:normal}.long-vector i:nth-child(-n+2){border-bottom:5px solid #00d4aa}.long-vector i:nth-child(n+3):nth-child(-n+4){border-bottom:5px solid #a78bfa}.long-vector i:nth-child(n+5):nth-child(-n+6){border-bottom:5px solid #f59e0b}.long-vector i:nth-child(n+7){border-bottom:5px solid #ef4444}
.long-vector em{font-size:30px;margin-left:10px}.slice-guide{position:absolute;top:135px;left:40px;width:760px;display:flex;gap:21px}.slice-guide i{width:155px;border-top:3px dashed #8b9dc3}.slice-guide span{position:absolute;right:-210px;top:-12px;color:#8b9dc3;font-size:20px}
.codebook-row{display:flex;gap:30px;margin-top:100px}.codebook{width:180px;height:145px;padding:17px;background:#151f37;border:1px solid rgba(139,157,195,.18);border-radius:15px}.codebook span{display:block;font-size:18px;color:#8b9dc3;margin-bottom:14px}.codebook i{display:inline-block;width:36px;height:70px;margin-right:9px;border-radius:6px;background:#263655}.codebook i:nth-child(2){background:#00d4aa}.codebook:nth-child(2) i:nth-child(3){background:#a78bfa}.codebook:nth-child(3) i:nth-child(4){background:#f59e0b}.codebook:nth-child(4) i:nth-child(2){background:#ef4444}
.short-code{position:absolute;right:45px;top:60px}.short-code b{font-size:30px;color:#00d4aa}.memory-compare{position:absolute;left:40px;right:45px;bottom:30px;padding:22px 28px;background:#151f37;border-radius:18px}
.memory-compare>div{display:grid;grid-template-columns:135px 1fr;align-items:center;margin:10px 0}.memory-compare span{font-size:19px;color:#8b9dc3}.bar{display:block;height:20px;border-radius:99px;background:#a78bfa}.bar.compact{width:24%;background:#00d4aa}
.memory-compare b{position:absolute;right:28px;top:25px;color:#00d4aa;font-size:24px}.memory-compare em{position:absolute;right:28px;bottom:24px;color:#8b9dc3;font-size:18px;font-style:normal}
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;padding-top:30px}.kpi-card{height:440px;padding:26px;background:#151f37;border:1px solid rgba(139,157,195,.18);border-radius:20px}
.kpi-card>span{font:800 18px monospace;color:#8b9dc3}.kpi-card>strong{display:block;font-size:29px;margin-top:12px}.kpi-card em{display:block;font-size:19px;font-style:normal;color:#8b9dc3;text-align:center;margin-top:18px}
.ring{width:180px;height:180px;margin:35px auto 0;border-radius:50%;display:flex;align-items:center;justify-content:center;font:900 52px monospace;border:22px solid #00d4aa;border-right-color:#263655}.ring small{font-size:24px}
.bars{height:190px;display:flex;align-items:flex-end;justify-content:center;gap:14px;margin-top:28px}.bars i{width:34px;background:#a78bfa;border-radius:6px 6px 0 0}.bars i:nth-child(1){height:25%}.bars i:nth-child(2){height:48%}.bars i:nth-child(3){height:64%}.bars i:nth-child(4){height:84%}.bars i:nth-child(5){height:100%;background:#00d4aa}
.latency svg{width:100%;height:190px;margin-top:20px}.memory-stack{width:190px;height:190px;margin:25px auto 0;display:flex;flex-direction:column-reverse;gap:8px}.memory-stack i{height:38px;border-radius:6px;background:#f59e0b}.memory-stack i:nth-child(4){opacity:.35}.memory-stack i:nth-child(3){opacity:.55}.memory-stack i:nth-child(2){opacity:.75}
.tradeoff{height:90px;margin-top:25px;padding:20px 30px;background:#1a2744;border-radius:16px;display:flex;align-items:center;gap:24px}.tradeoff span{color:#8b9dc3;font-size:20px}.tradeoff i{flex:1;height:12px;border-radius:99px;background:linear-gradient(90deg,#00d4aa,#f59e0b,#ef4444);position:relative}.tradeoff i:after{content:"";position:absolute;left:68%;top:-9px;width:30px;height:30px;border-radius:50%;background:#fff}.tradeoff strong{color:#00d4aa;font-size:22px}.tradeoff b{color:#f59e0b;font-size:22px}
.recap-board{height:100%;padding:30px 50px}.recap-flow{height:190px;display:flex;align-items:center;justify-content:center;gap:28px}.recap-flow>div{width:300px;height:150px;padding:22px;background:#151f37;border:1px solid rgba(0,212,170,.28);border-radius:18px}.recap-flow div span{font:800 20px monospace;color:#00d4aa}.recap-flow div strong{display:block;font-size:27px;margin-top:10px}.recap-flow div em{display:block;font-style:normal;color:#8b9dc3;font-size:18px;margin-top:8px}.recap-flow>i{width:90px;border-top:4px solid #00d4aa;position:relative}.recap-flow>i:after{content:"";position:absolute;right:-2px;top:-9px;border-left:14px solid #00d4aa;border-top:9px solid transparent;border-bottom:9px solid transparent}
.tool-row{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:26px}.tool-row span{padding:21px;text-align:center;border-radius:14px;background:#1a2744;color:#a78bfa;font:800 23px monospace}.tool-row b{font:600 17px sans-serif;color:#8b9dc3}
.next-card{height:190px;margin-top:35px;padding:34px 45px;border-radius:22px;background:linear-gradient(110deg,#162842,#1a2744);border:1px solid rgba(167,139,250,.4);position:relative}.next-card span{font-size:20px;color:#a78bfa;font-weight:800}.next-card strong{display:block;font-size:37px;margin-top:18px}.milvus-mark{position:absolute;right:70px;top:42px;width:120px;height:105px}.milvus-mark i{position:absolute;width:34px;height:88px;border:8px solid #00d4aa;border-radius:50%;transform:rotate(28deg)}.milvus-mark i:nth-child(2){left:37px;transform:rotate(-28deg)}.milvus-mark i:nth-child(3){left:74px;transform:rotate(28deg)}
.generic-board{height:100%;display:grid;grid-template-columns:repeat(2,1fr);gap:22px;padding:45px}.generic-point{padding:28px;background:#151f37;border:1px solid rgba(139,157,195,.2);border-radius:18px}.generic-point span{font:800 23px monospace;color:#00d4aa}.generic-point b{display:block;font-size:28px;margin-top:15px}
.story-comparison{height:100%;display:grid;grid-template-columns:1fr 105px 1fr;gap:24px;align-items:center;position:relative;padding:35px 70px 120px}
.story-side{height:360px;padding:35px;border-radius:24px;background:#151f37;border:1px solid rgba(139,157,195,.2);position:relative;overflow:hidden}.story-side span{font:800 20px monospace;color:#8b9dc3}.story-side strong{display:block;font-size:34px;line-height:1.45;margin-top:42px}.story-side i{position:absolute;left:35px;right:35px;bottom:35px;height:12px;border-radius:99px;background:#f59e0b}.story-side.cool i{background:#00d4aa}.story-side.warm{border-color:rgba(245,158,11,.35)}.story-side.cool{border-color:rgba(0,212,170,.35)}.story-vs{text-align:center;font:900 34px monospace;color:#8b9dc3}.story-takeaway{position:absolute;left:70px;right:70px;bottom:22px;height:90px;padding:22px 28px;border-radius:16px;background:#1a2744;display:flex;align-items:center;gap:30px}.story-takeaway span{color:#00d4aa;font-size:19px;font-weight:800}.story-takeaway b{font-size:26px}
.story-pipeline{height:100%;display:flex;align-items:center;justify-content:center;gap:19px;padding:55px}.story-step{width:280px;min-height:245px;padding:27px;background:#151f37;border:1px solid rgba(0,212,170,.25);border-radius:20px;display:flex;flex-direction:column;justify-content:center}.story-step span{font:900 22px monospace;color:#00d4aa}.story-step strong{font-size:27px;line-height:1.4;margin-top:25px}.story-flow{width:70px;border-top:4px solid #00d4aa;position:relative}.story-flow:after{content:"";position:absolute;right:-2px;top:-9px;border-left:14px solid #00d4aa;border-top:9px solid transparent;border-bottom:9px solid transparent}
.story-space{height:610px;margin:15px 90px;position:relative;border-left:3px solid #4b5d82;border-bottom:3px solid #4b5d82;background:radial-gradient(circle at 26% 32%,rgba(0,212,170,.1),transparent 24%),radial-gradient(circle at 70% 27%,rgba(167,139,250,.1),transparent 25%),radial-gradient(circle at 53% 70%,rgba(245,158,11,.1),transparent 24%)}.space-dot{position:absolute;width:29px;height:29px;border-radius:50%;background:#00d4aa}.space-dot.group-2{background:#a78bfa}.space-dot.group-3{background:#f59e0b}.space-label{position:absolute;padding:10px 16px;border-radius:9px;background:#1a2744;font-size:20px;font-weight:750;max-width:320px}.space-label.l1{left:13%;top:48%;color:#00d4aa}.space-label.l2{right:9%;top:42%;color:#a78bfa}.space-label.l3{left:45%;bottom:5%;color:#f59e0b}.space-query{position:absolute;left:46%;top:42%;width:64px;height:64px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#fff;color:#0f1729;font:900 25px monospace;border:8px solid #38bdf8}.space-links{position:absolute;inset:0;width:100%;height:100%}
.story-graph{height:100%;position:relative}.story-graph svg{position:absolute;inset:0;width:100%;height:100%}.story-node{position:absolute;transform:translate(-50%,-50%);width:230px;min-height:115px;padding:19px;border-radius:17px;background:#151f37;border:2px solid rgba(0,212,170,.35)}.story-node span{font:800 18px monospace;color:#00d4aa}.story-node b{display:block;font-size:20px;line-height:1.35;margin-top:8px}
.story-clusters{height:620px;position:relative;margin:10px 80px}.story-cluster{position:absolute;width:340px;height:240px;border:3px dashed #00d4aa;border-radius:48%;background:rgba(0,212,170,.05)}.story-cluster.violet{border-color:#a78bfa;background:rgba(167,139,250,.05)}.story-cluster.warm{border-color:#f59e0b;background:rgba(245,158,11,.05)}.story-cluster i{position:absolute;width:25px;height:25px;border-radius:50%;background:#00d4aa}.story-cluster.violet i{background:#a78bfa}.story-cluster.warm i{background:#f59e0b}.story-cluster i:nth-child(1){left:22%;top:30%}.story-cluster i:nth-child(2){left:54%;top:22%}.story-cluster i:nth-child(3){left:38%;top:58%}.story-cluster i:nth-child(4){left:70%;top:63%}.story-cluster strong{position:absolute;left:20px;right:20px;bottom:18px;text-align:center;font-size:20px}.cluster-query{position:absolute;left:49%;top:43%;width:65px;height:65px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#fff;color:#0f1729;font:900 25px monospace;border:8px solid #38bdf8}
.story-compression{height:100%;display:grid;grid-template-columns:1fr 280px 1fr;align-items:center;gap:35px;padding:60px 90px}.compression-box{height:390px;padding:30px;border-radius:22px;background:#151f37;border:1px solid rgba(139,157,195,.2)}.compression-box.before{border-color:rgba(167,139,250,.35)}.compression-box.after{border-color:rgba(0,212,170,.35)}.compression-box span{font:800 19px monospace;color:#8b9dc3}.compression-box strong{display:block;font-size:30px;line-height:1.4;margin-top:28px}.data-bars{display:flex;gap:10px;align-items:flex-end;height:130px;margin-top:34px}.data-bars i{width:35px;height:100%;border-radius:7px;background:#a78bfa}.data-bars i:nth-child(2n){height:72%}.data-bars.compact i{height:44%;background:#00d4aa}.compression-process{text-align:center}.compression-process b{display:block;font-size:24px;color:#f59e0b}.compression-process i{display:block;font-style:normal;font-size:75px;color:#f59e0b;margin-top:20px}
.story-terminal{height:580px;margin:25px 110px;border-radius:20px;overflow:hidden;background:#0a1020;border:1px solid rgba(139,157,195,.25);box-shadow:0 25px 70px rgba(0,0,0,.35)}.story-terminal header{height:58px;background:#1a2744;display:flex;align-items:center;gap:10px;padding:0 22px}.story-terminal header i{width:15px;height:15px;border-radius:50%;background:#ef4444}.story-terminal header i:nth-child(2){background:#f59e0b}.story-terminal header i:nth-child(3){background:#00d4aa}.story-terminal header span{margin-left:14px;color:#8b9dc3;font:600 16px monospace}.story-terminal main{padding:25px 32px}.terminal-line{display:grid;grid-template-columns:55px 1fr;gap:18px;padding:15px 0;border-bottom:1px solid rgba(139,157,195,.11)}.terminal-line span{font:600 17px monospace;color:#4b5d82}.terminal-line code{font:600 22px/1.4 "JetBrains Mono",monospace;color:#e8edf5}.story-terminal footer{margin:0 32px;padding:17px 20px;border-radius:10px;background:rgba(0,212,170,.1);color:#8b9dc3;font-size:18px}.story-terminal footer b{color:#00d4aa;margin-right:12px}
.story-architecture{height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center}.arch-client,.arch-storage{min-width:430px;padding:18px 28px;text-align:center;border-radius:13px;background:#1a2744;color:#8b9dc3;font-size:21px}.arch-arrow{font-style:normal;font-size:37px;color:#00d4aa;margin:10px}.arch-grid{width:1180px;display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.arch-block{min-height:135px;padding:22px;border-radius:16px;background:#151f37;border:1px solid rgba(0,212,170,.24)}.arch-block span{font:800 18px monospace;color:#00d4aa}.arch-block strong{display:block;font-size:22px;line-height:1.35;margin-top:13px}.arch-storage{border:1px solid rgba(167,139,250,.3);color:#a78bfa}
.story-dashboard{height:100%;display:grid;grid-template-columns:repeat(5,1fr);gap:18px;align-items:center;padding:45px}.story-kpi{height:410px;padding:25px;background:#151f37;border:1px solid color-mix(in srgb,var(--accent) 38%,transparent);border-top:5px solid var(--accent);border-radius:18px}.story-kpi>span{font:800 19px monospace;color:var(--accent)}.story-kpi>strong{display:block;font-size:24px;line-height:1.38;margin-top:23px;min-height:135px}.story-kpi>div{height:140px;display:flex;align-items:flex-end;gap:11px}.story-kpi i{flex:1;border-radius:5px 5px 0 0;background:var(--accent);opacity:.85}
.story-diagnosis{height:100%;display:grid;grid-template-columns:1fr 90px 1fr 90px 1fr;align-items:center;gap:15px;padding:70px}.diagnosis-step{height:360px;padding:35px;border-radius:22px;background:#151f37;border:1px solid rgba(139,157,195,.2)}.diagnosis-step span{display:inline-block;padding:9px 15px;border-radius:99px;background:rgba(239,68,68,.13);color:#ef4444;font-size:19px;font-weight:800}.diagnosis-step.cause span{background:rgba(245,158,11,.13);color:#f59e0b}.diagnosis-step.fix span{background:rgba(0,212,170,.13);color:#00d4aa}.diagnosis-step strong{display:block;font-size:30px;line-height:1.45;margin-top:50px}.story-diagnosis>i{font-style:normal;text-align:center;font-size:50px;color:#4b5d82}
.story-recap{height:100%;display:flex;align-items:center;justify-content:center}.recap-orbit{width:1250px;min-height:470px;position:relative;display:flex;align-items:center;justify-content:center}.recap-core{width:300px;height:170px;display:flex;align-items:center;justify-content:center;text-align:center;padding:25px;border-radius:50%;background:#1a2744;border:3px solid #00d4aa;font-size:28px;font-weight:850;box-shadow:0 0 55px rgba(0,212,170,.12)}.recap-item{position:absolute;width:300px;min-height:115px;padding:20px;border-radius:16px;background:#151f37;border:1px solid rgba(167,139,250,.28)}.recap-item:nth-child(2){left:0;top:25px}.recap-item:nth-child(3){right:0;top:25px}.recap-item:nth-child(4){left:0;bottom:25px}.recap-item:nth-child(5){right:0;bottom:25px}.recap-item:nth-child(6){left:50%;bottom:-25px;transform:translateX(-50%)}.recap-item span{font:800 18px monospace;color:#a78bfa}.recap-item strong{display:block;font-size:21px;line-height:1.35;margin-top:9px}
.subtitle-layer{position:absolute;z-index:100;left:0;right:0;bottom:0;height:100px;background:rgba(7,13,27,.94);border-top:1px solid rgba(0,212,170,.28)}
.subtitle-text{position:absolute;left:5%;right:5%;top:50%;transform:translateY(-50%);text-align:center;font-size:33px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;opacity:0}
"""


def generate_html(chapter_dir: Path, output: Path | None = None) -> Path:
    storyboard = read_storyboard(chapter_dir / "storyboard.md")
    narration_text = (chapter_dir / "narration.txt").read_text(encoding="utf-8")
    paragraphs = [part.strip() for part in narration_text.split("\n\n") if part.strip()]
    timing = json.loads((chapter_dir / "narration_timing.json").read_text(encoding="utf-8"))
    scenes = storyboard.get("scenes", [])
    timing_scenes = timing.get("scenes", [])
    chapter = storyboard.get("chapter", "00")

    if not (len(scenes) == len(paragraphs) == len(timing_scenes)):
        raise ValueError(
            f"Scene 数不一致: storyboard={len(scenes)}, narration={len(paragraphs)}, timing={len(timing_scenes)}"
        )

    total_duration = float(timing["total_duration"])
    normalized_scenes: list[dict] = []
    scene_html: list[str] = []
    timeline: list[str] = []

    for index, (scene, item) in enumerate(zip(scenes, timing_scenes, strict=True)):
        start = float(item["start"])
        next_start = (
            float(timing_scenes[index + 1]["start"])
            if index + 1 < len(timing_scenes)
            else total_duration
        )
        duration = round(next_start - start, 2)
        normalized_scenes.append({"start": start, "duration": duration})
        scene_html.append(render_scene(chapter, index + 1, scene, item, duration))

        timeline.append(
            f'tl.fromTo("#scene-{index + 1} .scene-header", {{opacity:0,y:-18}}, '
            f'{{opacity:1,y:0,duration:.45,ease:"power3.out"}}, {start + 0.12:.2f});'
        )
        beats = scene.get("beats", [])
        for beat_index, beat in enumerate(beats, start=1):
            beat_time = start + duration * float(beat["at"])
            selector = f"#scene-{index + 1} .beat-{beat_index}"
            timeline.append(
                f'tl.fromTo("{selector}", {{opacity:0,y:26,scale:.985}}, '
                f'{{opacity:1,y:0,scale:1,duration:.55,ease:"power3.out"}}, {beat_time:.2f});'
            )

    subtitle_html, subtitle_timeline = render_subtitles(normalized_scenes, paragraphs)
    timeline.append(subtitle_timeline)

    comp_id = f"chapter-{chapter}-storyboard"
    document = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Chapter {chapter} {html.escape(storyboard.get("title", ""))}</title>
</head>
<body>
<div data-composition-id="{comp_id}" data-start="0" data-duration="{total_duration:.2f}"
     data-width="1920" data-height="1080">
  <audio id="narration" data-start="0" data-duration="{total_duration:.2f}"
         data-track-index="0" src="narration.mp3" data-volume="1"></audio>
  {''.join(scene_html)}
  <div id="subtitle-layer" class="subtitle-layer clip" data-start="0"
       data-duration="{total_duration:.2f}" data-track-index="99">
    {subtitle_html}
  </div>
</div>
<style>{CSS}</style>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
window.__timelines = window.__timelines || {{}};
(function(){{
  const tl = gsap.timeline({{paused:true}});
  {' '.join(timeline)}
  window.__timelines["{comp_id}"] = tl;
}})();
</script>
</body>
</html>
"""
    document = "\n".join(line.rstrip() for line in document.splitlines()) + "\n"
    output_path = output or chapter_dir / "index.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(document, encoding="utf-8")
    print(
        f"Generated: {output_path} "
        f"({total_duration:.2f}s, {len(scenes)} scenes, {len(document)} bytes)"
    )
    return output_path


def media_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def validate_workspace(chapter_dir: Path, video: Path | None = None) -> None:
    storyboard = read_storyboard(chapter_dir / "storyboard.md")
    paragraphs = [
        part.strip()
        for part in (chapter_dir / "narration.txt").read_text(encoding="utf-8").split("\n\n")
        if part.strip()
    ]
    timing = json.loads((chapter_dir / "narration_timing.json").read_text(encoding="utf-8"))
    scenes = storyboard.get("scenes", [])
    timing_scenes = timing.get("scenes", [])
    document = (chapter_dir / "index.html").read_text(encoding="utf-8")

    errors: list[str] = []
    if not (len(scenes) == len(paragraphs) == len(timing_scenes)):
        errors.append("storyboard、旁白和 timing 的 Scene 数不一致")
    if document.count('class="scene clip') != len(scenes):
        errors.append("HTML Scene 数与 storyboard 不一致")
    if storyboard.get("chapter") == "01":
        if "轿车和香蕉，哪个更像卡车" not in document:
            errors.append("HTML 未包含新版轿车/香蕉/卡车示例")
        if "苹果和香蕉" in document or "哪个更像橘子" in document:
            errors.append("HTML 仍包含旧水果示例")
    if 'motion_canvas = false' not in (chapter_dir / "storyboard.md").read_text(encoding="utf-8"):
        errors.append("storyboard 未保持 motion_canvas=false")

    audio_duration = media_duration(chapter_dir / "narration.mp3")
    timing_duration = float(timing["total_duration"])
    if abs(audio_duration - timing_duration) > 0.15:
        errors.append(
            f"音频与 timing 总时长偏差过大: audio={audio_duration:.3f}, timing={timing_duration:.3f}"
        )

    if video:
        video_duration = media_duration(video)
        if abs(video_duration - audio_duration) > 0.35:
            errors.append(
                f"视频与音频总时长偏差过大: video={video_duration:.3f}, audio={audio_duration:.3f}"
            )
    else:
        video_duration = None

    if errors:
        raise RuntimeError("\n".join(errors))

    summary = (
        f"Validated: scenes={len(scenes)}, audio={audio_duration:.2f}s, "
        f"timing={timing_duration:.2f}s"
    )
    if video_duration is not None:
        summary += f", video={video_duration:.2f}s"
    print(summary)


def main() -> int:
    parser = argparse.ArgumentParser(description="分镜驱动的 HyperFrames HTML 生成与验证工具")
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare_parser = subparsers.add_parser("prepare", help="创建独立章节测试工作区")
    prepare_parser.add_argument("source_dir", type=Path)
    prepare_parser.add_argument("output_dir", type=Path)

    render_parser = subparsers.add_parser("render", help="根据分镜和 timing 生成 index.html")
    render_parser.add_argument("chapter_dir", type=Path)
    render_parser.add_argument("--output", type=Path)

    validate_parser = subparsers.add_parser("validate", help="验证章节生成产物")
    validate_parser.add_argument("chapter_dir", type=Path)
    validate_parser.add_argument("--video", type=Path)

    args = parser.parse_args()
    if args.command == "prepare":
        prepare_workspace(args.source_dir.resolve(), args.output_dir.resolve())
    elif args.command == "render":
        generate_html(args.chapter_dir.resolve(), args.output.resolve() if args.output else None)
    elif args.command == "validate":
        validate_workspace(
            args.chapter_dir.resolve(),
            args.video.resolve() if args.video else None,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
