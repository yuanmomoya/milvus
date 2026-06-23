# Chapter XX 视频分镜

> 本文件同时供人审阅和批量生成器读取。TOML 代码块是机器数据源；代码块外可以补充创作说明，
> 但不能替代或覆盖代码块中的字段。

## 课程定位

- 对应教程：`../../milvus-master-course/docs/XX-章节标题.md`
- 目标受众：填写本章适合的人群
- 核心问题：填写本章要解决的问题
- 学完能够：填写 2-4 个可验证的学习结果

## 分镜数据

```toml
schema_version = 1
chapter = "XX"
title = "章节标题"
source_doc = "../../milvus-master-course/docs/XX-章节标题.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "场景标题"
purpose = "hook"
visual_type = "hook-comparison"
layout = "split"
key_points = ["屏幕短句一", "屏幕短句二"]
components = ["component-a", "component-b"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "component-a"
description = "场景开始时显示主要问题"

[[scenes.beats]]
at = 0.35
action = "draw"
target = "component-b"
description = "绘制核心关系"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "key-result"
description = "突出本场景结论"
```

## 人工检查

- [ ] Scene 数量与 `narration.txt` 段落数量一致
- [ ] `narration_index` 从 1 连续递增
- [ ] 每个 Beat 的 `at` 处于 `0.0-1.0` 且严格递增
- [ ] 屏幕文字是知识摘要，没有复制整段旁白
- [ ] 每个技术概念都有对应视觉表达
- [ ] 代码场景使用真实代码或命令，不使用伪造 API
- [ ] 最后一个场景包含本章总结和下一章预告
- [ ] `renderer = "hyperframes"` 且 `motion_canvas = false`
