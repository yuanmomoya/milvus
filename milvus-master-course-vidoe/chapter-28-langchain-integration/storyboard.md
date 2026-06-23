# Chapter 28 LangChain 集成视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/28-LangChain集成.md`
- 核心问题：用可视化方式讲清《28 LangChain 集成》中的关键概念、工程流程与选择依据
- 场景数量：7 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "28"
title = "LangChain 集成"
source_doc = "../../milvus-master-course/docs/28-LangChain集成.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "LangChain是目前最流行的LLM应用框架，它把M…"
purpose = "hook"
visual_type = "learning-map"
layout = "full"
key_points = ["上一章我们手动实现了Agent，这一章用LangChain框架来简化集成", "LangChain是目前最流行的LLM应用框架，它把Milvus封装成了Vecto…", "我们看怎么用、有什么坑、什么时候该用什么时候不该用"]
components = ["chapter-map", "learning-goals", "progress-path"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "chapter-map"
description = "建立场景主题：上一章我们手动实现了Agent，这一章用LangChain框架来简化集成"

[[scenes.beats]]
at = 0.36
action = "connect"
target = "learning-goals"
description = "用动态图解展开：LangChain是目前最流行的LLM应用框架，它把Milvus封装成了Vecto…"

[[scenes.beats]]
at = 0.72
action = "preview"
target = "progress-path"
description = "突出结论并承接下一段：我们看怎么用、有什么坑、什么时候该用什么时候不该用"

[[scenes]]
id = "s02"
narration_index = 2
title = "LangChain集成Milvus的核心是Milvus…"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["LangChain集成Milvus的核心是Milvus类，在langchain_m…", "初始化时传入Embedding模型和连接参数，它会自动创建Collection、建…", "写入用add_documents，检索用similarity_search或as_…"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：LangChain集成Milvus的核心是Milvus类，在langchain_m…"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：初始化时传入Embedding模型和连接参数，它会自动创建Collection、建…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：写入用add_documents，检索用similarity_search或as_…"

[[scenes]]
id = "s03"
narration_index = 3
title = "一个典型的RAG链路用LangChain怎么写"
purpose = "demo"
visual_type = "pipeline"
layout = "diagram"
key_points = ["一个典型的RAG链路用LangChain怎么写", "四步", "第一步，初始化Milvus向量存储"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：一个典型的RAG链路用LangChain怎么写"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：四步"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：第一步，初始化Milvus向量存储"

[[scenes]]
id = "s04"
narration_index = 4
title = "LangChain的好处是什么"
purpose = "concept"
visual_type = "vector-space"
layout = "diagram"
key_points = ["LangChain的好处是什么", "开发速度快", "标准化的接口让你可以快速切换不同的向量数据库、不同的LLM、不同的Embeddin…"]
components = ["vector-points", "query-node", "distance-lines", "topk-ring"]

[[scenes.beats]]
at = 0.00
action = "scatter"
target = "vector-points"
description = "建立场景主题：LangChain的好处是什么"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "query-node"
description = "用动态图解展开：开发速度快"

[[scenes.beats]]
at = 0.72
action = "select"
target = "distance-lines"
description = "突出结论并承接下一段：标准化的接口让你可以快速切换不同的向量数据库、不同的LLM、不同的Embeddin…"

[[scenes]]
id = "s05"
narration_index = 5
title = "LangChain的坑在哪"
purpose = "diagnosis"
visual_type = "code-terminal"
layout = "code"
key_points = ["LangChain的坑在哪", "第一，抽象泄漏", "LangChain的Milvus封装隐藏了很多细节，比如索引参数、搜索参数、Sch…"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：LangChain的坑在哪"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：第一，抽象泄漏"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：LangChain的Milvus封装隐藏了很多细节，比如索引参数、搜索参数、Sch…"

[[scenes]]
id = "s06"
narration_index = 6
title = "什么时候用LangChain，什么时候直接用pymil…"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["什么时候用LangChain，什么时候直接用pymilvus", "快速原型、标准RAG流程、需要频繁切换组件时用LangChain", "对性能要求高、需要精细控制索引和搜索参数、或者架构比较定制时直接用pymilvus"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：什么时候用LangChain，什么时候直接用pymilvus"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：快速原型、标准RAG流程、需要频繁切换组件时用LangChain"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：对性能要求高、需要精细控制索引和搜索参数、或者架构比较定制时直接用pymilvus"

[[scenes]]
id = "s07"
narration_index = 7
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "LangChain让Milvus集成变得简单：几行代码搞定RAG", "但要理解它的抽象边界——简单场景用框架，复杂场景用原生API"]
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
description = "用动态图解展开：LangChain让Milvus集成变得简单：几行代码搞定RAG"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：但要理解它的抽象边界——简单场景用框架，复杂场景用原生API"
```

## 人工检查

- [x] 7 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
