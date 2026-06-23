# Chapter 26 多路召回架构视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/26-多路召回架构.md`
- 核心问题：用可视化方式讲清《26 多路召回架构》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "26"
title = "多路召回架构"
source_doc = "../../milvus-master-course/docs/26-多路召回架构.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "前面几章我们分别学了语义搜索、关键词匹配、Query…"
purpose = "hook"
visual_type = "hook-comparison"
layout = "split"
key_points = ["前面几章我们分别学了语义搜索、关键词匹配、Query Rewrite、Rerank", "这一章把它们整合成多路召回架构", "它适合单一路径覆盖不足的RAG系统：多条检索路径并行，结果融合后重排序，再选择少量…"]
components = ["question-card", "before-after-panels", "conflict-highlight"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "question-card"
description = "建立场景主题：前面几章我们分别学了语义搜索、关键词匹配、Query Rewrite、Rerank"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "before-after-panels"
description = "用动态图解展开：这一章把它们整合成多路召回架构"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "conflict-highlight"
description = "突出结论并承接下一段：它适合单一路径覆盖不足的RAG系统：多条检索路径并行，结果融合后重排序，再选择少量…"

[[scenes]]
id = "s02"
narration_index = 2
title = "多路召回的架构长这样"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["多路召回的架构长这样", "用户问题进来，先做Query Rewrite生成多个查询变体", "然后每个变体走多条检索路径：稠密向量搜索、稀疏向量搜索、标题向量搜索"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：多路召回的架构长这样"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：用户问题进来，先做Query Rewrite生成多个查询变体"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：然后每个变体走多条检索路径：稠密向量搜索、稀疏向量搜索、标题向量搜索"

[[scenes]]
id = "s03"
narration_index = 3
title = "为什么要多路"
purpose = "concept"
visual_type = "dashboard"
layout = "dashboard"
key_points = ["为什么要多路", "因为单一路径总有盲区", "语义搜索擅长理解意图但可能漏掉精确关键词"]
components = ["metric-cards", "trend-chart", "threshold-line", "tradeoff-control"]

[[scenes.beats]]
at = 0.00
action = "reveal"
target = "metric-cards"
description = "建立场景主题：为什么要多路"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "trend-chart"
description = "用动态图解展开：因为单一路径总有盲区"

[[scenes.beats]]
at = 0.72
action = "balance"
target = "threshold-line"
description = "突出结论并承接下一段：语义搜索擅长理解意图但可能漏掉精确关键词"

[[scenes]]
id = "s04"
narration_index = 4
title = "融合策略怎么选"
purpose = "comparison"
visual_type = "metric-comparison"
layout = "split"
key_points = ["融合策略怎么选", "RRF是最稳的选择", "它不依赖分数的绝对值，只看排名"]
components = ["comparison-cards", "tradeoff-axis", "decision-marker"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "comparison-cards"
description = "建立场景主题：融合策略怎么选"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "tradeoff-axis"
description = "用动态图解展开：RRF是最稳的选择"

[[scenes.beats]]
at = 0.72
action = "decide"
target = "decision-marker"
description = "突出结论并承接下一段：它不依赖分数的绝对值，只看排名"

[[scenes]]
id = "s05"
narration_index = 5
title = "实现上有几个工程细节"
purpose = "demo"
visual_type = "code-terminal"
layout = "code"
key_points = ["实现上有几个工程细节", "第一，各路检索要并行执行，不能串行，否则延迟叠加", "用Python的asyncio或线程池并发调用"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：实现上有几个工程细节"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：第一，各路检索要并行执行，不能串行，否则延迟叠加"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：用Python的asyncio或线程池并发调用"

[[scenes]]
id = "s06"
narration_index = 6
title = "权重怎么调"
purpose = "concept"
visual_type = "dashboard"
layout = "dashboard"
key_points = ["权重怎么调", "如果用WeightedRanker，需要给每路分配权重", "初始可以均匀分配，然后用测试集评估"]
components = ["metric-cards", "trend-chart", "threshold-line", "tradeoff-control"]

[[scenes.beats]]
at = 0.00
action = "reveal"
target = "metric-cards"
description = "建立场景主题：权重怎么调"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "trend-chart"
description = "用动态图解展开：如果用WeightedRanker，需要给每路分配权重"

[[scenes.beats]]
at = 0.72
action = "balance"
target = "threshold-line"
description = "突出结论并承接下一段：初始可以均匀分配，然后用测试集评估"

[[scenes]]
id = "s07"
narration_index = 7
title = "性能考虑"
purpose = "concept"
visual_type = "dashboard"
layout = "dashboard"
key_points = ["性能考虑", "多路召回的延迟取决于最慢的那一路", "如果稀疏向量搜索比稠密向量慢很多，整体延迟就被拖慢"]
components = ["metric-cards", "trend-chart", "threshold-line", "tradeoff-control"]

[[scenes.beats]]
at = 0.00
action = "reveal"
target = "metric-cards"
description = "建立场景主题：性能考虑"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "trend-chart"
description = "用动态图解展开：多路召回的延迟取决于最慢的那一路"

[[scenes.beats]]
at = 0.72
action = "balance"
target = "threshold-line"
description = "突出结论并承接下一段：如果稀疏向量搜索比稠密向量慢很多，整体延迟就被拖慢"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "多路召回的核心是路径互补、并行执行、融合去重和必要时的Rerank", "它可能提升召回率，也会增加延迟、成本和调试复杂度，提升幅度必须由离线评测决定"]
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
description = "用动态图解展开：多路召回的核心是路径互补、并行执行、融合去重和必要时的Rerank"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：它可能提升召回率，也会增加延迟、成本和调试复杂度，提升幅度必须由离线评测决定"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
