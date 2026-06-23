# Chapter 07 向量数据建模视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/07-向量数据建模.md`
- 核心问题：用可视化方式讲清《07 向量数据建模》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "07"
title = "向量数据建模"
source_doc = "../../milvus-master-course/docs/07-向量数据建模.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "核心问题是：除了向量本身，还需要保存什么信息"
purpose = "hook"
visual_type = "hook-comparison"
layout = "split"
key_points = ["上一章我们设计了Collection的Schema，这一章往里填内容：向量数据建模", "核心问题是：除了向量本身，还需要保存什么信息", "我们分三种场景来看：文本、图片、多模态"]
components = ["question-card", "before-after-panels", "conflict-highlight"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "question-card"
description = "建立场景主题：上一章我们设计了Collection的Schema，这一章往里填内容：向量数据建模"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "before-after-panels"
description = "用动态图解展开：核心问题是：除了向量本身，还需要保存什么信息"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "conflict-highlight"
description = "突出结论并承接下一段：我们分三种场景来看：文本、图片、多模态"

[[scenes]]
id = "s02"
narration_index = 2
title = "先看文本建模，这是最常见的场景"
purpose = "concept"
visual_type = "code-terminal"
layout = "code"
key_points = ["先看文本建模，这是最常见的场景", "一篇长文档不能直接存，要先切成Chunk", "每个Chunk就是一条记录"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：先看文本建模，这是最常见的场景"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：一篇长文档不能直接存，要先切成Chunk"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：每个Chunk就是一条记录"

[[scenes]]
id = "s03"
narration_index = 3
title = "文本切分有讲究"
purpose = "concept"
visual_type = "metric-comparison"
layout = "split"
key_points = ["文本切分有讲究", "切太长，向量表达不精确，因为一段话里可能有多个主题", "切太短，丢失上下文，搜索结果断章取义"]
components = ["comparison-cards", "tradeoff-axis", "decision-marker"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "comparison-cards"
description = "建立场景主题：文本切分有讲究"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "tradeoff-axis"
description = "用动态图解展开：切太长，向量表达不精确，因为一段话里可能有多个主题"

[[scenes.beats]]
at = 0.72
action = "decide"
target = "decision-marker"
description = "突出结论并承接下一段：切太短，丢失上下文，搜索结果断章取义"

[[scenes]]
id = "s04"
narration_index = 4
title = "图片建模和文本不一样"
purpose = "concept"
visual_type = "vector-space"
layout = "diagram"
key_points = ["图片建模和文本不一样", "图片的元数据是尺寸、格式、标签、版权信息", "图片本身不存在Milvus里，存的是图片的URL或路径"]
components = ["vector-points", "query-node", "distance-lines", "topk-ring"]

[[scenes.beats]]
at = 0.00
action = "scatter"
target = "vector-points"
description = "建立场景主题：图片建模和文本不一样"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "query-node"
description = "用动态图解展开：图片的元数据是尺寸、格式、标签、版权信息"

[[scenes.beats]]
at = 0.72
action = "select"
target = "distance-lines"
description = "突出结论并承接下一段：图片本身不存在Milvus里，存的是图片的URL或路径"

[[scenes]]
id = "s05"
narration_index = 5
title = "多模态建模更复杂一些"
purpose = "concept"
visual_type = "code-terminal"
layout = "code"
key_points = ["多模态建模更复杂一些", "同一个Collection里可能有文本和图片混在一起", "关键是它们必须在同一个向量空间里——也就是说，必须用同一个多模态模型编码"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：多模态建模更复杂一些"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：同一个Collection里可能有文本和图片混在一起"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：关键是它们必须在同一个向量空间里——也就是说，必须用同一个多模态模型编码"

[[scenes]]
id = "s06"
narration_index = 6
title = "不管哪种场景，都要考虑数据的生命周期"
purpose = "concept"
visual_type = "vector-space"
layout = "diagram"
key_points = ["不管哪种场景，都要考虑数据的生命周期", "加一个created_at时间戳字段，方便按时间过滤和清理过期数据", "加一个model_version字段，记录用的哪个Embedding模型版本"]
components = ["vector-points", "query-node", "distance-lines", "topk-ring"]

[[scenes.beats]]
at = 0.00
action = "scatter"
target = "vector-points"
description = "建立场景主题：不管哪种场景，都要考虑数据的生命周期"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "query-node"
description = "用动态图解展开：加一个created_at时间戳字段，方便按时间过滤和清理过期数据"

[[scenes.beats]]
at = 0.72
action = "select"
target = "distance-lines"
description = "突出结论并承接下一段：加一个model_version字段，记录用的哪个Embedding模型版本"

[[scenes]]
id = "s07"
narration_index = 7
title = "说数据清洗"
purpose = "diagnosis"
visual_type = "error-diagnosis"
layout = "diagram"
key_points = ["最后说数据清洗", "入库前要做三件事：去重、标准化、校验维度", "去重靠主键的内容哈希"]
components = ["symptom-card", "diagnosis-tree", "fix-checklist"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "symptom-card"
description = "建立场景主题：最后说数据清洗"

[[scenes.beats]]
at = 0.36
action = "trace"
target = "diagnosis-tree"
description = "用动态图解展开：入库前要做三件事：去重、标准化、校验维度"

[[scenes.beats]]
at = 0.72
action = "resolve"
target = "fix-checklist"
description = "突出结论并承接下一段：去重靠主键的内容哈希"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "向量数据建模的核心是三层：检索层决定搜什么，展示层决定返回什么，管理层决定怎么维护", "想清楚这三层，Schema自然就出来了"]
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
description = "用动态图解展开：向量数据建模的核心是三层：检索层决定搜什么，展示层决定返回什么，管理层决定怎么维护"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：想清楚这三层，Schema自然就出来了"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
