# Chapter 16 批量写入优化视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/16-批量写入优化.md`
- 核心问题：用可视化方式讲清《16 批量写入优化》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "16"
title = "批量写入优化"
source_doc = "../../milvus-master-course/docs/16-批量写入优化.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "前面几章我们一直在聊怎么搜，这一章换个方向：怎么写"
purpose = "hook"
visual_type = "hook-comparison"
layout = "split"
key_points = ["前面几章我们一直在聊怎么搜，这一章换个方向：怎么写", "当你要往Milvus里灌几百万甚至几千万条数据时，一条一条写太慢了", "批量写入优化要解决三个问题：batch_size怎么选、Segment碎片怎么避免…"]
components = ["question-card", "before-after-panels", "conflict-highlight"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "question-card"
description = "建立场景主题：前面几章我们一直在聊怎么搜，这一章换个方向：怎么写"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "before-after-panels"
description = "用动态图解展开：当你要往Milvus里灌几百万甚至几千万条数据时，一条一条写太慢了"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "conflict-highlight"
description = "突出结论并承接下一段：批量写入优化要解决三个问题：batch_size怎么选、Segment碎片怎么避免…"

[[scenes]]
id = "s02"
narration_index = 2
title = "batch_size"
purpose = "demo"
visual_type = "code-terminal"
layout = "code"
key_points = ["batch_size", "每次upsert调用传入的数据条数就是batch_size", "太小，网络开销占比高，吞吐上不去"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：batch_size"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：每次upsert调用传入的数据条数就是batch_size"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：太小，网络开销占比高，吞吐上不去"

[[scenes]]
id = "s03"
narration_index = 3
title = "写入流程是这样的：数据进入WAL，再由Streamin…"
purpose = "concept"
visual_type = "dashboard"
layout = "dashboard"
key_points = ["写入流程是这样的：数据进入WAL，再由Streaming Node维护growin…", "growing segment达到条件后seal并flush成sealed seg…", "频繁手动flush会直接制造小segment"]
components = ["metric-cards", "trend-chart", "threshold-line", "tradeoff-control"]

[[scenes.beats]]
at = 0.00
action = "reveal"
target = "metric-cards"
description = "建立场景主题：写入流程是这样的：数据进入WAL，再由Streaming Node维护growin…"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "trend-chart"
description = "用动态图解展开：growing segment达到条件后seal并flush成sealed seg…"

[[scenes.beats]]
at = 0.72
action = "balance"
target = "threshold-line"
description = "突出结论并承接下一段：频繁手动flush会直接制造小segment"

[[scenes]]
id = "s04"
narration_index = 4
title = "怎么避免Segment碎片"
purpose = "concept"
visual_type = "metric-comparison"
layout = "split"
key_points = ["怎么避免Segment碎片", "第一，不要手动调flush，让Milvus自动管理", "第二，batch_size不要太小"]
components = ["comparison-cards", "tradeoff-axis", "decision-marker"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "comparison-cards"
description = "建立场景主题：怎么避免Segment碎片"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "tradeoff-axis"
description = "用动态图解展开：第一，不要手动调flush，让Milvus自动管理"

[[scenes.beats]]
at = 0.72
action = "decide"
target = "decision-marker"
description = "突出结论并承接下一段：第二，batch_size不要太小"

[[scenes]]
id = "s05"
narration_index = 5
title = "写入吞吐怎么优化"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["写入吞吐怎么优化", "几个技巧", "第一，从较小并发度开始压测，线程过多也可能造成连接、WAL或服务端竞争"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：写入吞吐怎么优化"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：几个技巧"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：第一，从较小并发度开始压测，线程过多也可能造成连接、WAL或服务端竞争"

[[scenes]]
id = "s06"
narration_index = 6
title = "还有个生产级的模式：断点续传"
purpose = "concept"
visual_type = "code-terminal"
layout = "code"
key_points = ["还有个生产级的模式：断点续传", "大批量写入可能中途失败", "用upsert加内容哈希主键，天然支持重试——失败了从断点重跑，已写入的数据会被覆…"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：还有个生产级的模式：断点续传"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：大批量写入可能中途失败"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：用upsert加内容哈希主键，天然支持重试——失败了从断点重跑，已写入的数据会被覆…"

[[scenes]]
id = "s07"
narration_index = 7
title = "说一个坑：写入和搜索的资源竞争"
purpose = "diagnosis"
visual_type = "architecture"
layout = "diagram"
key_points = ["最后说一个坑：写入和搜索的资源竞争", "大批量写入时，Streaming Node、IndexNode、对象存储和网络都会…", "生产环境建议在低峰期做批量导入，或通过资源隔离和限流控制影响"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：最后说一个坑：写入和搜索的资源竞争"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：大批量写入时，Streaming Node、IndexNode、对象存储和网络都会…"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：生产环境建议在低峰期做批量导入，或通过资源隔离和限流控制影响"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "批量写入的核心是：合理的batch_size、避免Segment碎片、受控并发，并…", "这些方法通常能提升吞吐，但具体能从多久降到多久必须由数据大小、硬件和索引配置决定"]
components = ["knowledge-map", "chapter-progress", "next-chapter-card"]

[[scenes.beats]]
at = 0.00
action = "assemble"
target = "knowledge-map"
description = "建立场景主题：好，总结一下"

[[scenes.beats]]
at = 0.36
action = "recap"
target = "chapter-progress"
description = "用动态图解展开：批量写入的核心是：合理的batch_size、避免Segment碎片、受控并发，并…"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：这些方法通常能提升吞吐，但具体能从多久降到多久必须由数据大小、硬件和索引配置决定"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
