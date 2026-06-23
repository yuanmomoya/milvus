# Chapter 13 混合检索 HybridSearch视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/13-混合检索HybridSearch.md`
- 核心问题：用可视化方式讲清《13 混合检索 HybridSearch》中的关键概念、工程流程与选择依据
- 场景数量：7 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "13"
title = "混合检索 HybridSearch"
source_doc = "../../milvus-master-course/docs/13-混合检索HybridSearch.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "前面几章我们一直在聊纯向量搜索"
purpose = "hook"
visual_type = "learning-map"
layout = "full"
key_points = ["前面几章我们一直在聊纯向量搜索", "但实际业务中，纯语义搜索有一个常见局限：它可能漏掉版本号、错误码和专有名词的精确匹配", "比如用户搜\"pymilvus 2.4 upsert bug\"，语义搜索可能偏向写入…"]
components = ["chapter-map", "learning-goals", "progress-path"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "chapter-map"
description = "建立场景主题：前面几章我们一直在聊纯向量搜索"

[[scenes.beats]]
at = 0.36
action = "connect"
target = "learning-goals"
description = "用动态图解展开：但实际业务中，纯语义搜索有一个常见局限：它可能漏掉版本号、错误码和专有名词的精确匹配"

[[scenes.beats]]
at = 0.72
action = "preview"
target = "progress-path"
description = "突出结论并承接下一段：比如用户搜\"pymilvus 2.4 upsert bug\"，语义搜索可能偏向写入…"

[[scenes]]
id = "s02"
narration_index = 2
title = "混合检索的核心思路是多路召回加融合"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["混合检索的核心思路是多路召回加融合", "第一路用稠密向量做语义搜索，找语义相关的结果", "第二路用稀疏向量做关键词匹配，找词汇精确匹配的结果"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：混合检索的核心思路是多路召回加融合"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：第一路用稠密向量做语义搜索，找语义相关的结果"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：第二路用稀疏向量做关键词匹配，找词汇精确匹配的结果"

[[scenes]]
id = "s03"
narration_index = 3
title = "稀疏向量是什么"
purpose = "concept"
visual_type = "metric-comparison"
layout = "split"
key_points = ["稀疏向量是什么", "它和稠密向量不同", "稠密向量每个维度都有值，比如768维全是浮点数"]
components = ["comparison-cards", "tradeoff-axis", "decision-marker"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "comparison-cards"
description = "建立场景主题：稀疏向量是什么"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "tradeoff-axis"
description = "用动态图解展开：它和稠密向量不同"

[[scenes.beats]]
at = 0.72
action = "decide"
target = "decision-marker"
description = "突出结论并承接下一段：稠密向量每个维度都有值，比如768维全是浮点数"

[[scenes]]
id = "s04"
narration_index = 4
title = "在Milvus里怎么做混合检索"
purpose = "concept"
visual_type = "code-terminal"
layout = "code"
key_points = ["在Milvus里怎么做混合检索", "Schema里定义两个向量字段：一个FLOAT_VECTOR存稠密向量，一个SPA…", "搜索时用hybrid_search方法，传入两个搜索请求，Milvus内部分别执行…"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：在Milvus里怎么做混合检索"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：Schema里定义两个向量字段：一个FLOAT_VECTOR存稠密向量，一个SPA…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：搜索时用hybrid_search方法，传入两个搜索请求，Milvus内部分别执行…"

[[scenes]]
id = "s05"
narration_index = 5
title = "融合策略有两种"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["融合策略有两种", "RRF，Reciprocal Rank Fusion：按排名倒数加权，不需要分数归…", "WeightedRanker：按分数加权，需要指定每路的权重，比如语义0.7、关键…"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：融合策略有两种"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：RRF，Reciprocal Rank Fusion：按排名倒数加权，不需要分数归…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：WeightedRanker：按分数加权，需要指定每路的权重，比如语义0.7、关键…"

[[scenes]]
id = "s06"
narration_index = 6
title = "除了稠密加稀疏，还可以做多字段混合"
purpose = "concept"
visual_type = "vector-space"
layout = "diagram"
key_points = ["除了稠密加稀疏，还可以做多字段混合", "比如title_embedding和body_embedding两个稠密向量字段…", "标题匹配权重高一些，正文匹配权重低一些"]
components = ["vector-points", "query-node", "distance-lines", "topk-ring"]

[[scenes.beats]]
at = 0.00
action = "scatter"
target = "vector-points"
description = "建立场景主题：除了稠密加稀疏，还可以做多字段混合"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "query-node"
description = "用动态图解展开：比如title_embedding和body_embedding两个稠密向量字段…"

[[scenes.beats]]
at = 0.72
action = "select"
target = "distance-lines"
description = "突出结论并承接下一段：标题匹配权重高一些，正文匹配权重低一些"

[[scenes]]
id = "s07"
narration_index = 7
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "混合检索解决的是纯语义搜索的漏召回问题", "核心是多路召回加融合"]
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
description = "用动态图解展开：混合检索解决的是纯语义搜索的漏召回问题"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：核心是多路召回加融合"
```

## 人工检查

- [x] 7 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
