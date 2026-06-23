# Chapter 25 Rerank 重排序视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/25-Rerank重排序.md`
- 核心问题：用可视化方式讲清《25 Rerank 重排序》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "25"
title = "Rerank 重排序"
source_doc = "../../milvus-master-course/docs/25-Rerank重排序.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "但TopK个结果的排序可能不是最优的——向量相似度高不…"
purpose = "hook"
visual_type = "hook-comparison"
layout = "split"
key_points = ["上一章我们优化了召回，能找到更多相关文档了", "但TopK个结果的排序可能不是最优的——向量相似度高不一定意味着对回答问题最有帮助", "这一章我们加Rerank重排序：用一个更精确的模型对召回结果重新打分排序"]
components = ["question-card", "before-after-panels", "conflict-highlight"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "question-card"
description = "建立场景主题：上一章我们优化了召回，能找到更多相关文档了"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "before-after-panels"
description = "用动态图解展开：但TopK个结果的排序可能不是最优的——向量相似度高不一定意味着对回答问题最有帮助"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "conflict-highlight"
description = "突出结论并承接下一段：这一章我们加Rerank重排序：用一个更精确的模型对召回结果重新打分排序"

[[scenes]]
id = "s02"
narration_index = 2
title = "为什么需要Rerank"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["为什么需要Rerank", "向量检索是双塔模型：问题和文档分别编码，用向量距离衡量相关性", "这种方式快但粗糙"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：为什么需要Rerank"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：向量检索是双塔模型：问题和文档分别编码，用向量距离衡量相关性"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：这种方式快但粗糙"

[[scenes]]
id = "s03"
narration_index = 3
title = "典型的流程是：先用向量检索召回Top50，再用Rera…"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["典型的流程是：先用向量检索召回Top50，再用Rerank模型对这50条重新打分…", "这样既利用了向量检索的速度，又利用了Rerank的精度", "两阶段架构：粗排加精排"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：典型的流程是：先用向量检索召回Top50，再用Rerank模型对这50条重新打分…"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：这样既利用了向量检索的速度，又利用了Rerank的精度"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：两阶段架构：粗排加精排"

[[scenes]]
id = "s04"
narration_index = 4
title = "Rerank模型怎么选"
purpose = "concept"
visual_type = "code-terminal"
layout = "code"
key_points = ["Rerank模型怎么选", "中文场景推荐bge-reranker-base或bge-reranker-large", "API方式可以用Cohere的rerank接口"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：Rerank模型怎么选"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：中文场景推荐bge-reranker-base或bge-reranker-large"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：API方式可以用Cohere的rerank接口"

[[scenes]]
id = "s05"
narration_index = 5
title = "代码流程并不复杂"
purpose = "demo"
visual_type = "code-terminal"
layout = "code"
key_points = ["代码流程并不复杂", "加载CrossEncoder模型，传入问题和文档列表，得到分数列表，按分数降序排列…", "Rerank是否提升答案质量要通过评测验证，而且模型大小、候选数量、批处理和硬件都…"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：代码流程并不复杂"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：加载CrossEncoder模型，传入问题和文档列表，得到分数列表，按分数降序排列…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：Rerank是否提升答案质量要通过评测验证，而且模型大小、候选数量、批处理和硬件都…"

[[scenes]]
id = "s06"
narration_index = 6
title = "Rerank的调优点"
purpose = "concept"
visual_type = "dashboard"
layout = "dashboard"
key_points = ["Rerank的调优点", "第一，召回数量：给Rerank的候选集要够大，通常Top20到Top50", "太少可能漏掉好结果，太多Rerank延迟太高"]
components = ["metric-cards", "trend-chart", "threshold-line", "tradeoff-control"]

[[scenes.beats]]
at = 0.00
action = "reveal"
target = "metric-cards"
description = "建立场景主题：Rerank的调优点"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "trend-chart"
description = "用动态图解展开：第一，召回数量：给Rerank的候选集要够大，通常Top20到Top50"

[[scenes.beats]]
at = 0.72
action = "balance"
target = "threshold-line"
description = "突出结论并承接下一段：太少可能漏掉好结果，太多Rerank延迟太高"

[[scenes]]
id = "s07"
narration_index = 7
title = "一个常见误区：以为Rerank能弥补召回的不足"
purpose = "concept"
visual_type = "dashboard"
layout = "dashboard"
key_points = ["一个常见误区：以为Rerank能弥补召回的不足", "如果正确文档根本不在Top50里，Rerank也救不了", "Rerank只能改善排序，不能凭空创造结果"]
components = ["metric-cards", "trend-chart", "threshold-line", "tradeoff-control"]

[[scenes.beats]]
at = 0.00
action = "reveal"
target = "metric-cards"
description = "建立场景主题：一个常见误区：以为Rerank能弥补召回的不足"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "trend-chart"
description = "用动态图解展开：如果正确文档根本不在Top50里，Rerank也救不了"

[[scenes.beats]]
at = 0.72
action = "balance"
target = "threshold-line"
description = "突出结论并承接下一段：Rerank只能改善排序，不能凭空创造结果"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "Rerank是RAG精度的最后一公里", "粗排用向量检索保速度，精排用交叉编码器保精度"]
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
description = "用动态图解展开：Rerank是RAG精度的最后一公里"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：粗排用向量检索保速度，精排用交叉编码器保精度"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
