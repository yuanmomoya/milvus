# Chapter 22 RAG 架构基础视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/22-RAG架构基础.md`
- 核心问题：用可视化方式讲清《22 RAG 架构基础》中的关键概念、工程流程与选择依据
- 场景数量：7 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "22"
title = "RAG 架构基础"
source_doc = "../../milvus-master-course/docs/22-RAG架构基础.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "从这一章开始我们进入RAG专题"
purpose = "hook"
visual_type = "hook-comparison"
layout = "split"
key_points = ["从这一章开始我们进入RAG专题", "RAG是Retrieval Augmented Generation的缩写，检索增…", "简单说就是：先从知识库里检索相关内容，再把检索结果喂给大模型生成答案"]
components = ["question-card", "before-after-panels", "conflict-highlight"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "question-card"
description = "建立场景主题：从这一章开始我们进入RAG专题"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "before-after-panels"
description = "用动态图解展开：RAG是Retrieval Augmented Generation的缩写，检索增…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "conflict-highlight"
description = "突出结论并承接下一段：简单说就是：先从知识库里检索相关内容，再把检索结果喂给大模型生成答案"

[[scenes]]
id = "s02"
narration_index = 2
title = "为什么需要RAG"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["为什么需要RAG", "大模型有三个硬伤", "第一，知识有截止日期，训练数据之后的事它不知道"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：为什么需要RAG"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：大模型有三个硬伤"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：第一，知识有截止日期，训练数据之后的事它不知道"

[[scenes]]
id = "s03"
narration_index = 3
title = "RAG的核心流程分两个阶段"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["RAG的核心流程分两个阶段", "离线阶段：把文档切成Chunk，用Embedding模型编码成向量，存入Milvus", "在线阶段：用户提问，把问题编码成向量，从Milvus检索TopK个相关Chunk…"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：RAG的核心流程分两个阶段"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：离线阶段：把文档切成Chunk，用Embedding模型编码成向量，存入Milvus"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：在线阶段：用户提问，把问题编码成向量，从Milvus检索TopK个相关Chunk…"

[[scenes]]
id = "s04"
narration_index = 4
title = "离线阶段的关键是文档处理"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["离线阶段的关键是文档处理", "原始文档可能是PDF、Word、网页、Markdown", "先解析成纯文本，再切成Chunk"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：离线阶段的关键是文档处理"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：原始文档可能是PDF、Word、网页、Markdown"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：先解析成纯文本，再切成Chunk"

[[scenes]]
id = "s05"
narration_index = 5
title = "在线阶段的关键是Prompt工程"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["在线阶段的关键是Prompt工程", "检索到的Chunk要合理组织：按相关度排序，去重，控制总长度不超过模型的上下文窗口", "Prompt模板通常是：这是相关的参考资料加Chunk内容，然后请根据以上资料回答…"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：在线阶段的关键是Prompt工程"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：检索到的Chunk要合理组织：按相关度排序，去重，控制总长度不超过模型的上下文窗口"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：Prompt模板通常是：这是相关的参考资料加Chunk内容，然后请根据以上资料回答…"

[[scenes]]
id = "s06"
narration_index = 6
title = "RAG的效果取决于三个环节"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["RAG的效果取决于三个环节", "检索质量：能不能找到真正相关的Chunk", "Chunk质量：切分是否合理，信息是否完整"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：RAG的效果取决于三个环节"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：检索质量：能不能找到真正相关的Chunk"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：Chunk质量：切分是否合理，信息是否完整"

[[scenes]]
id = "s07"
narration_index = 7
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "RAG等于检索加生成", "Milvus负责检索这一环，大模型负责生成那一环"]
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
description = "用动态图解展开：RAG等于检索加生成"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：Milvus负责检索这一环，大模型负责生成那一环"
```

## 人工检查

- [x] 7 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
