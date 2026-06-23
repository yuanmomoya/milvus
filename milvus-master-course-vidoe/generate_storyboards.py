"""根据每章旁白和教程文档批量生成可机器解析的 storyboard.md。"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path

BASE = Path(__file__).parent
COURSE_DOCS = BASE.parent / "milvus-master-course" / "docs"


@dataclass(frozen=True)
class VisualSpec:
    visual_type: str
    layout: str
    components: tuple[str, ...]
    actions: tuple[str, str, str]


VISUAL_SPECS = {
    "hook-comparison": VisualSpec(
        "hook-comparison",
        "split",
        ("question-card", "before-after-panels", "conflict-highlight"),
        ("show", "compare", "highlight"),
    ),
    "learning-map": VisualSpec(
        "learning-map",
        "full",
        ("chapter-map", "learning-goals", "progress-path"),
        ("show", "connect", "preview"),
    ),
    "pipeline": VisualSpec(
        "pipeline",
        "diagram",
        ("flow-nodes", "data-packets", "result-card"),
        ("show", "flow", "highlight"),
    ),
    "vector-space": VisualSpec(
        "vector-space",
        "diagram",
        ("vector-points", "query-node", "distance-lines", "topk-ring"),
        ("scatter", "measure", "select"),
    ),
    "metric-comparison": VisualSpec(
        "metric-comparison",
        "split",
        ("comparison-cards", "tradeoff-axis", "decision-marker"),
        ("show", "compare", "decide"),
    ),
    "graph-search": VisualSpec(
        "graph-search",
        "diagram",
        ("graph-layers", "search-route", "candidate-nodes"),
        ("build", "traverse", "arrive"),
    ),
    "cluster-search": VisualSpec(
        "cluster-search",
        "diagram",
        ("clusters", "centroids", "query-node", "selected-regions"),
        ("cluster", "probe", "select"),
    ),
    "compression": VisualSpec(
        "compression",
        "diagram",
        ("source-vector", "segments", "codebook", "memory-bars"),
        ("show", "encode", "compare"),
    ),
    "code-terminal": VisualSpec(
        "code-terminal",
        "code",
        ("code-editor", "terminal-output", "callout-labels"),
        ("type", "execute", "highlight"),
    ),
    "architecture": VisualSpec(
        "architecture",
        "diagram",
        ("service-nodes", "request-path", "storage-layer"),
        ("build", "route", "focus"),
    ),
    "dashboard": VisualSpec(
        "dashboard",
        "dashboard",
        ("metric-cards", "trend-chart", "threshold-line", "tradeoff-control"),
        ("reveal", "measure", "balance"),
    ),
    "error-diagnosis": VisualSpec(
        "error-diagnosis",
        "diagram",
        ("symptom-card", "diagnosis-tree", "fix-checklist"),
        ("show", "trace", "resolve"),
    ),
    "recap": VisualSpec(
        "recap",
        "full",
        ("knowledge-map", "chapter-progress", "next-chapter-card"),
        ("assemble", "recap", "transition"),
    ),
}


def split_sentences(text: str) -> list[str]:
    return [
        part.strip()
        for part in re.split(r"(?<=[。！？；])", text)
        if part.strip()
    ]


def clean_title(text: str) -> str:
    sentences = split_sentences(text)
    title = sentences[0] if sentences else text
    if title.startswith("上一章") and len(sentences) > 1:
        title = sentences[1]
    title = re.sub(r"^(先来|先说|接下来|再说|然后|好，|最后|回顾一下，?)", "", title)
    title = title.strip("，。！？：； ")
    if len(title) > 28:
        title = title[:27].rstrip("，、：； ") + "…"
    return title or "核心概念"


def short_point(sentence: str, limit: int = 42) -> str:
    sentence = sentence.strip("，。！？； ")
    sentence = re.sub(r"^(上一章[^。！？]*[。！？]|接下来|先说|再说|具体来说[：，]?)", "", sentence)
    if len(sentence) > limit:
        return sentence[: limit - 1].rstrip("，、：； ") + "…"
    return sentence


def classify_visual(paragraph: str, scene_index: int, scene_count: int) -> VisualSpec:
    lower = paragraph.lower()
    if scene_index == scene_count:
        return VISUAL_SPECS["recap"]
    if scene_index == 1 and any(word in paragraph for word in ("想象", "问题", "如果", "为什么", "有没有")):
        return VISUAL_SPECS["hook-comparison"]
    if scene_index == 1:
        return VISUAL_SPECS["learning-map"]
    if any(word in lower for word in ("错误处理", "报错", "排查", "故障", "失败原因", "常见坑", "问题定位", "debug")):
        return VISUAL_SPECS["error-diagnosis"]
    if any(word in lower for word in ("hnsw", "图索引", "导航图", "邻接图", "源码调用")):
        return VISUAL_SPECS["graph-search"]
    if any(word in lower for word in ("pq", "sq8", "量化", "压缩", "码本", "int8")):
        return VISUAL_SPECS["compression"]
    if any(word in lower for word in ("ivf", "nlist", "nprobe", "聚类", "簇", "partition", "分区")):
        return VISUAL_SPECS["cluster-search"]
    if any(word in lower for word in ("proxy", "querynode", "datanode", "coord", "etcd", "minio", "架构", "集群", "副本", "高可用", "服务")):
        return VISUAL_SPECS["architecture"]
    if any(word in lower for word in ("代码", "python", "docker", "curl", "api", "fastapi", "milvusclient", "upsert", "insert", "search(", "query(", "schema")):
        return VISUAL_SPECS["code-terminal"]
    if any(word in lower for word in ("qps", "p99", "p95", "延迟", "吞吐", "监控", "指标", "benchmark", "压测", "召回率", "内存使用", "性能优化")):
        return VISUAL_SPECS["dashboard"]
    if any(word in lower for word in ("异步", "流程", "链路", "先", "然后", "接着", "写入", "检索", "召回", "生成", "处理")):
        return VISUAL_SPECS["pipeline"]
    if any(word in lower for word in ("embedding", "向量空间", "相似度", "topk", "clip", "多模态", "图片检索", "视频检索")):
        return VISUAL_SPECS["vector-space"]
    if any(word in paragraph for word in ("区别", "对比", "选哪个", "选择", "优缺点", "权衡", "适合", "不适合")):
        return VISUAL_SPECS["metric-comparison"]
    return VISUAL_SPECS["metric-comparison"]


def purpose_for(paragraph: str, scene_index: int, scene_count: int) -> str:
    if scene_index == 1:
        return "hook"
    if scene_index == scene_count:
        return "summary"
    if any(word in paragraph for word in ("错误处理", "报错", "坑", "排查", "故障")):
        return "diagnosis"
    if any(word in paragraph for word in ("代码", "怎么用", "实现", "命令", "调用")):
        return "demo"
    if any(word in paragraph for word in ("区别", "对比", "选择", "权衡")):
        return "comparison"
    return "concept"


def toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def toml_array(values: list[str] | tuple[str, ...]) -> str:
    return "[" + ", ".join(toml_string(value) for value in values) + "]"


def find_source_doc(chapter: str) -> Path:
    matches = sorted(COURSE_DOCS.glob(f"{chapter}-*.md"))
    if len(matches) != 1:
        raise ValueError(f"Chapter {chapter}: 对应教程文档数量不是 1: {matches}")
    return matches[0]


def build_storyboard(chapter_dir: Path) -> str:
    chapter = chapter_dir.name.split("-", 2)[1]
    source_doc = find_source_doc(chapter)
    doc_title = source_doc.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
    narration = (chapter_dir / "narration.txt").read_text(encoding="utf-8")
    paragraphs = [part.strip() for part in narration.split("\n\n") if part.strip()]
    timing = json.loads((chapter_dir / "narration_timing.json").read_text(encoding="utf-8"))
    if len(paragraphs) != len(timing["scenes"]):
        raise ValueError(
            f"{chapter_dir.name}: narration={len(paragraphs)} timing={len(timing['scenes'])}"
        )

    lines = [
        f"# Chapter {chapter} {doc_title.removeprefix(chapter).strip()}视频分镜",
        "",
        "## 课程定位",
        "",
        f"- 对应教程：`../../milvus-master-course/docs/{source_doc.name}`",
        f"- 核心问题：用可视化方式讲清《{doc_title}》中的关键概念、工程流程与选择依据",
        f"- 场景数量：{len(paragraphs)} 个 Scene，与旁白段落和 timing 一一对应",
        "",
        "## 分镜数据",
        "",
        "```toml",
        "schema_version = 1",
        f"chapter = {toml_string(chapter)}",
        f"title = {toml_string(doc_title.removeprefix(chapter).strip())}",
        f"source_doc = {toml_string('../../milvus-master-course/docs/' + source_doc.name)}",
        'narration_file = "narration.txt"',
        'timing_file = "narration_timing.json"',
        'renderer = "hyperframes"',
        "motion_canvas = false",
    ]

    for index, paragraph in enumerate(paragraphs, start=1):
        sentences = split_sentences(paragraph)
        points = [short_point(sentence) for sentence in sentences[:3]]
        points = [point for point in points if point]
        if not points:
            points = [clean_title(paragraph)]
        spec = classify_visual(paragraph, index, len(paragraphs))
        purpose = purpose_for(paragraph, index, len(paragraphs))
        title = clean_title(paragraph)
        lines.extend(
            [
                "",
                "[[scenes]]",
                f'id = "s{index:02d}"',
                f"narration_index = {index}",
                f"title = {toml_string(title)}",
                f"purpose = {toml_string(purpose)}",
                f"visual_type = {toml_string(spec.visual_type)}",
                f"layout = {toml_string(spec.layout)}",
                f"key_points = {toml_array(points)}",
                f"components = {toml_array(spec.components)}",
            ]
        )
        beat_times = (0.00, 0.36, 0.72)
        beat_descriptions = (
            f"建立场景主题：{points[0]}",
            f"用动态图解展开：{points[min(1, len(points) - 1)]}",
            f"突出结论并承接下一段：{points[-1]}",
        )
        for beat_time, action, component, description in zip(
            beat_times,
            spec.actions,
            spec.components[:3],
            beat_descriptions,
            strict=True,
        ):
            lines.extend(
                [
                    "",
                    "[[scenes.beats]]",
                    f"at = {beat_time:.2f}",
                    f"action = {toml_string(action)}",
                    f"target = {toml_string(component)}",
                    f"description = {toml_string(description)}",
                ]
            )

    lines.extend(
        [
            "```",
            "",
            "## 人工检查",
            "",
            f"- [x] {len(paragraphs)} 个 Scene 与旁白、timing 数量一致",
            "- [x] 所有 Beat 使用 `0.0-1.0` 相对时间",
            "- [x] 使用受控视觉类型和可复用组件",
            "- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾",
            "- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="覆盖已经存在的 storyboard.md；默认保留人工精修版本",
    )
    parser.add_argument(
        "--include-manual",
        action="store_true",
        help="允许覆盖第一章等人工精修分镜；默认始终保留 chapter-01",
    )
    args = parser.parse_args()
    generated = 0
    skipped = 0
    for chapter_dir in sorted(BASE.glob("chapter-*")):
        if not chapter_dir.is_dir():
            continue
        output = chapter_dir / "storyboard.md"
        if chapter_dir.name.startswith("chapter-01-") and output.exists() and not args.include_manual:
            print(f"SKIP {chapter_dir.name}: 保留人工精修 storyboard.md")
            skipped += 1
            continue
        if output.exists() and not args.overwrite:
            print(f"SKIP {chapter_dir.name}: storyboard.md 已存在")
            skipped += 1
            continue
        output.write_text(build_storyboard(chapter_dir), encoding="utf-8")
        print(f"WRITE {output.relative_to(BASE)}")
        generated += 1
    print(f"Done: generated={generated}, skipped={skipped}")


if __name__ == "__main__":
    main()
