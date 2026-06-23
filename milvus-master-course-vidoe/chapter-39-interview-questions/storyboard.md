# Chapter 39 Milvus 面试题大全视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/39-Milvus面试题大全.md`
- 核心问题：用可视化方式讲清《39 Milvus 面试题大全》中的关键概念、工程流程与选择依据
- 场景数量：9 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "39"
title = "Milvus 面试题大全"
source_doc = "../../milvus-master-course/docs/39-Milvus面试题大全.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "这一章是面试题大全"
purpose = "hook"
visual_type = "hook-comparison"
layout = "split"
key_points = ["这一章是面试题大全", "不是死记硬背的题库，而是帮你检验前面三十八章的理解深度", "每个问题背后都对应一个核心概念"]
components = ["question-card", "before-after-panels", "conflict-highlight"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "question-card"
description = "建立场景主题：这一章是面试题大全"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "before-after-panels"
description = "用动态图解展开：不是死记硬背的题库，而是帮你检验前面三十八章的理解深度"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "conflict-highlight"
description = "突出结论并承接下一段：每个问题背后都对应一个核心概念"

[[scenes]]
id = "s02"
narration_index = 2
title = "第一类：基础概念"
purpose = "comparison"
visual_type = "vector-space"
layout = "diagram"
key_points = ["第一类：基础概念", "向量数据库和传统数据库的本质区别是什么", "Embedding模型的作用是什么"]
components = ["vector-points", "query-node", "distance-lines", "topk-ring"]

[[scenes.beats]]
at = 0.00
action = "scatter"
target = "vector-points"
description = "建立场景主题：第一类：基础概念"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "query-node"
description = "用动态图解展开：向量数据库和传统数据库的本质区别是什么"

[[scenes.beats]]
at = 0.72
action = "select"
target = "distance-lines"
description = "突出结论并承接下一段：Embedding模型的作用是什么"

[[scenes]]
id = "s03"
narration_index = 3
title = "第二类：索引原理"
purpose = "comparison"
visual_type = "graph-search"
layout = "diagram"
key_points = ["第二类：索引原理", "HNSW的多层图结构是怎么加速搜索的", "IVF的nlist和nprobe分别控制什么"]
components = ["graph-layers", "search-route", "candidate-nodes"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "graph-layers"
description = "建立场景主题：第二类：索引原理"

[[scenes.beats]]
at = 0.36
action = "traverse"
target = "search-route"
description = "用动态图解展开：HNSW的多层图结构是怎么加速搜索的"

[[scenes.beats]]
at = 0.72
action = "arrive"
target = "candidate-nodes"
description = "突出结论并承接下一段：IVF的nlist和nprobe分别控制什么"

[[scenes]]
id = "s04"
narration_index = 4
title = "第三类：Milvus架构"
purpose = "comparison"
visual_type = "architecture"
layout = "diagram"
key_points = ["第三类：Milvus架构", "Proxy、Coord、Node各自的职责是什么", "写入成功和可被搜索之间为什么有时间差"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：第三类：Milvus架构"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：Proxy、Coord、Node各自的职责是什么"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：写入成功和可被搜索之间为什么有时间差"

[[scenes]]
id = "s05"
narration_index = 5
title = "第四类：生产实践"
purpose = "diagnosis"
visual_type = "error-diagnosis"
layout = "diagram"
key_points = ["第四类：生产实践", "Collection的主键应该怎么设计", "批量写入的最佳实践是什么"]
components = ["symptom-card", "diagnosis-tree", "fix-checklist"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "symptom-card"
description = "建立场景主题：第四类：生产实践"

[[scenes.beats]]
at = 0.36
action = "trace"
target = "diagnosis-tree"
description = "用动态图解展开：Collection的主键应该怎么设计"

[[scenes.beats]]
at = 0.72
action = "resolve"
target = "fix-checklist"
description = "突出结论并承接下一段：批量写入的最佳实践是什么"

[[scenes]]
id = "s06"
narration_index = 6
title = "第五类：RAG相关"
purpose = "comparison"
visual_type = "pipeline"
layout = "diagram"
key_points = ["第五类：RAG相关", "RAG解决了大模型的什么问题", "文档切分策略怎么选"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：第五类：RAG相关"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：RAG解决了大模型的什么问题"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：文档切分策略怎么选"

[[scenes]]
id = "s07"
narration_index = 7
title = "第六类：系统设计"
purpose = "demo"
visual_type = "pipeline"
layout = "diagram"
key_points = ["第六类：系统设计", "设计一个支持十亿向量的检索系统，你会怎么做", "如何实现多租户隔离"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：第六类：系统设计"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：设计一个支持十亿向量的检索系统，你会怎么做"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：如何实现多租户隔离"

[[scenes]]
id = "s08"
narration_index = 8
title = "回答面试题的技巧"
purpose = "comparison"
visual_type = "pipeline"
layout = "diagram"
key_points = ["回答面试题的技巧", "第一，先说结论再展开", "第二，用具体数字：不说\"很多\"，说\"一百万条768维向量需要约3G内存\""]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：回答面试题的技巧"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：第一，先说结论再展开"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：第二，用具体数字：不说\"很多\"，说\"一百万条768维向量需要约3G内存\""

[[scenes]]
id = "s09"
narration_index = 9
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "面试题的本质是检验你对系统的理解深度", "不是背答案，是理解原理后自然能回答"]
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
description = "用动态图解展开：面试题的本质是检验你对系统的理解深度"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：不是背答案，是理解原理后自然能回答"
```

## 人工检查

- [x] 9 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
