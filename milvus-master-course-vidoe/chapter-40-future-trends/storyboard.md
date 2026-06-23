# Chapter 40 未来趋势与生态视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/40-未来趋势与生态.md`
- 核心问题：用可视化方式讲清《40 未来趋势与生态》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "40"
title = "未来趋势与生态"
source_doc = "../../milvus-master-course/docs/40-未来趋势与生态.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "恭喜你走到了最后一章"
purpose = "hook"
visual_type = "learning-map"
layout = "full"
key_points = ["恭喜你走到了最后一章", "前面三十九章从向量基础到生产实战，从单机到集群，从文本到多模态，覆盖了Milvus…", "这一章我们展望未来：向量数据库的发展趋势、Milvus的路线图、以及整个AI基础设…"]
components = ["chapter-map", "learning-goals", "progress-path"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "chapter-map"
description = "建立场景主题：恭喜你走到了最后一章"

[[scenes.beats]]
at = 0.36
action = "connect"
target = "learning-goals"
description = "用动态图解展开：前面三十九章从向量基础到生产实战，从单机到集群，从文本到多模态，覆盖了Milvus…"

[[scenes.beats]]
at = 0.72
action = "preview"
target = "progress-path"
description = "突出结论并承接下一段：这一章我们展望未来：向量数据库的发展趋势、Milvus的路线图、以及整个AI基础设…"

[[scenes]]
id = "s02"
narration_index = 2
title = "第一个趋势：向量数据库和传统数据库的融合"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["第一个趋势：向量数据库和传统数据库的融合", "PostgreSQL有了pgvector，Redis有了向量搜索模块，Elasti…", "未来可能不需要单独部署向量数据库，通用数据库就能满足基本的向量检索需求"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：第一个趋势：向量数据库和传统数据库的融合"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：PostgreSQL有了pgvector，Redis有了向量搜索模块，Elasti…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：未来可能不需要单独部署向量数据库，通用数据库就能满足基本的向量检索需求"

[[scenes]]
id = "s03"
narration_index = 3
title = "第二个趋势：GPU加速会覆盖更多高吞吐场景"
purpose = "concept"
visual_type = "dashboard"
layout = "dashboard"
key_points = ["第二个趋势：GPU加速会覆盖更多高吞吐场景", "GPU不只是用来训练模型，也可以用于向量检索", "是否值得采用取决于数据规模、批量度、延迟目标和成本"]
components = ["metric-cards", "trend-chart", "threshold-line", "tradeoff-control"]

[[scenes.beats]]
at = 0.00
action = "reveal"
target = "metric-cards"
description = "建立场景主题：第二个趋势：GPU加速会覆盖更多高吞吐场景"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "trend-chart"
description = "用动态图解展开：GPU不只是用来训练模型，也可以用于向量检索"

[[scenes.beats]]
at = 0.72
action = "balance"
target = "threshold-line"
description = "突出结论并承接下一段：是否值得采用取决于数据规模、批量度、延迟目标和成本"

[[scenes]]
id = "s04"
narration_index = 4
title = "第三个趋势：多模态原生支持"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["第三个趋势：多模态原生支持", "现在做多模态检索需要自己处理不同模态的编码和对齐", "未来向量数据库可能原生支持多模态数据类型，内置多模态Embedding，自动处理跨…"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：第三个趋势：多模态原生支持"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：现在做多模态检索需要自己处理不同模态的编码和对齐"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：未来向量数据库可能原生支持多模态数据类型，内置多模态Embedding，自动处理跨…"

[[scenes]]
id = "s05"
narration_index = 5
title = "第四个趋势：和大模型的深度集成"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["第四个趋势：和大模型的深度集成", "RAG只是开始", "未来向量数据库可能成为大模型的长期记忆层：模型的对话历史、学习到的知识、用户偏好都…"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：第四个趋势：和大模型的深度集成"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：RAG只是开始"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：未来向量数据库可能成为大模型的长期记忆层：模型的对话历史、学习到的知识、用户偏好都…"

[[scenes]]
id = "s06"
narration_index = 6
title = "第五个趋势：Serverless和按需付费"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["第五个趋势：Serverless和按需付费", "不需要自己管理集群，按查询量和存储量付费", "Zilliz Cloud已经在做这个方向"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：第五个趋势：Serverless和按需付费"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：不需要自己管理集群，按查询量和存储量付费"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：Zilliz Cloud已经在做这个方向"

[[scenes]]
id = "s07"
narration_index = 7
title = "Milvus生态的现状"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["Milvus生态的现状", "pymilvus是Python SDK，还有Java、Go、Node.js的SDK", "Attu是可视化管理工具"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：Milvus生态的现状"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：pymilvus是Python SDK，还有Java、Go、Node.js的SDK"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：Attu是可视化管理工具"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下整个课程"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下整个课程", "从第一章的向量概念到最后一章的未来趋势，核心就一句话：向量检索是AI应用的基础设施", "掌握了Milvus，你就掌握了构建智能搜索、RAG、推荐系统、多模态应用的核心能力"]
components = ["knowledge-map", "chapter-progress", "next-chapter-card"]

[[scenes.beats]]
at = 0.00
action = "assemble"
target = "knowledge-map"
description = "建立场景主题：好，总结一下整个课程"

[[scenes.beats]]
at = 0.36
action = "recap"
target = "chapter-progress"
description = "用动态图解展开：从第一章的向量概念到最后一章的未来趋势，核心就一句话：向量检索是AI应用的基础设施"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：掌握了Milvus，你就掌握了构建智能搜索、RAG、推荐系统、多模态应用的核心能力"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
