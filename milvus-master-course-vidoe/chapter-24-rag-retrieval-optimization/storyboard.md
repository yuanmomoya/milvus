# Chapter 24 RAG 召回优化视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/24-RAG召回优化.md`
- 核心问题：用可视化方式讲清《24 RAG 召回优化》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "24"
title = "RAG 召回优化"
source_doc = "../../milvus-master-course/docs/24-RAG召回优化.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "最常见的问题是：用户问了一个问题，检索回来的Chunk…"
purpose = "hook"
visual_type = "hook-comparison"
layout = "split"
key_points = ["上一章我们搭建了基础RAG系统，能用但不够好", "最常见的问题是：用户问了一个问题，检索回来的Chunk不够相关，导致模型生成的答案…", "这一章我们优化召回：Query Rewrite、多路召回、父子Chunk、以及召回…"]
components = ["question-card", "before-after-panels", "conflict-highlight"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "question-card"
description = "建立场景主题：上一章我们搭建了基础RAG系统，能用但不够好"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "before-after-panels"
description = "用动态图解展开：最常见的问题是：用户问了一个问题，检索回来的Chunk不够相关，导致模型生成的答案…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "conflict-highlight"
description = "突出结论并承接下一段：这一章我们优化召回：Query Rewrite、多路召回、父子Chunk、以及召回…"

[[scenes]]
id = "s02"
narration_index = 2
title = "第一个优化：Query Rewrite，查询改写"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["第一个优化：Query Rewrite，查询改写", "用户的原始问题可能表述模糊或者用词和文档不一致", "比如用户问\"怎么让搜索更快\"，但文档里写的是\"查询性能调优\""]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：第一个优化：Query Rewrite，查询改写"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：用户的原始问题可能表述模糊或者用词和文档不一致"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：比如用户问\"怎么让搜索更快\"，但文档里写的是\"查询性能调优\""

[[scenes]]
id = "s03"
narration_index = 3
title = "第二个优化：多路召回"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["第二个优化：多路召回", "不只用一种方式检索", "第一路用稠密向量做语义搜索"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：第二个优化：多路召回"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：不只用一种方式检索"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：第一路用稠密向量做语义搜索"

[[scenes]]
id = "s04"
narration_index = 4
title = "第三个优化：父子Chunk策略"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["第三个优化：父子Chunk策略", "问题是：小Chunk检索精准但上下文不够，大Chunk上下文够但检索不精准", "解决方案是两层Chunk"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：第三个优化：父子Chunk策略"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：问题是：小Chunk检索精准但上下文不够，大Chunk上下文够但检索不精准"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：解决方案是两层Chunk"

[[scenes]]
id = "s05"
narration_index = 5
title = "第四个优化：Hypothetical Document…"
purpose = "demo"
visual_type = "pipeline"
layout = "diagram"
key_points = ["第四个优化：Hypothetical Document Embedding，假设文…", "思路是反过来：不是把问题变成向量去搜文档，而是让LLM先生成一个\"假设的理想答案\"…", "因为假设答案和真实文档的表述更接近，检索效果更好"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：第四个优化：Hypothetical Document Embedding，假设文…"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：思路是反过来：不是把问题变成向量去搜文档，而是让LLM先生成一个\"假设的理想答案\"…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：因为假设答案和真实文档的表述更接近，检索效果更好"

[[scenes]]
id = "s06"
narration_index = 6
title = "怎么评估召回质量"
purpose = "concept"
visual_type = "compression"
layout = "diagram"
key_points = ["怎么评估召回质量", "用标准的IR指标", "准备一个测试集：一组问题和对应的正确文档"]
components = ["source-vector", "segments", "codebook", "memory-bars"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "source-vector"
description = "建立场景主题：怎么评估召回质量"

[[scenes.beats]]
at = 0.36
action = "encode"
target = "segments"
description = "用动态图解展开：用标准的IR指标"

[[scenes.beats]]
at = 0.72
action = "compare"
target = "codebook"
description = "突出结论并承接下一段：准备一个测试集：一组问题和对应的正确文档"

[[scenes]]
id = "s07"
narration_index = 7
title = "一个实用的调试技巧：打印每次检索的结果和分数"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["一个实用的调试技巧：打印每次检索的结果和分数", "如果TopK结果的分数都很低，说明问题和文档的语义差距大，需要Query Rewr…", "如果分数高但内容不对，说明Embedding模型区分度不够，考虑换更好的模型"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：一个实用的调试技巧：打印每次检索的结果和分数"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：如果TopK结果的分数都很低，说明问题和文档的语义差距大，需要Query Rewr…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：如果分数高但内容不对，说明Embedding模型区分度不够，考虑换更好的模型"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "召回优化的四板斧：Query Rewrite改善问题表述、多路召回增加覆盖面、父子…", "下一章我们看Rerank重排序，进一步提升结果质量"]
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
description = "用动态图解展开：召回优化的四板斧：Query Rewrite改善问题表述、多路召回增加覆盖面、父子…"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：下一章我们看Rerank重排序，进一步提升结果质量"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
