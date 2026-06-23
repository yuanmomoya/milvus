# Chapter 38 源码阅读指南视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/38-源码阅读指南.md`
- 核心问题：用可视化方式讲清《38 源码阅读指南》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "38"
title = "源码阅读指南"
source_doc = "../../milvus-master-course/docs/38-源码阅读指南.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "前面三十七章我们一直在用Milvus，这一章我们打开它…"
purpose = "hook"
visual_type = "hook-comparison"
layout = "split"
key_points = ["前面三十七章我们一直在用Milvus，这一章我们打开它的源码看看里面是怎么实现的", "不是要你成为Milvus开发者，而是理解内部机制后，遇到问题能更快定位，做架构决策…"]
components = ["question-card", "before-after-panels", "conflict-highlight"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "question-card"
description = "建立场景主题：前面三十七章我们一直在用Milvus，这一章我们打开它的源码看看里面是怎么实现的"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "before-after-panels"
description = "用动态图解展开：不是要你成为Milvus开发者，而是理解内部机制后，遇到问题能更快定位，做架构决策…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "conflict-highlight"
description = "突出结论并承接下一段：不是要你成为Milvus开发者，而是理解内部机制后，遇到问题能更快定位，做架构决策…"

[[scenes]]
id = "s02"
narration_index = 2
title = "Milvus的源码在GitHub上，主要用Go语言写…"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["Milvus的源码在GitHub上，主要用Go语言写，搜索核心用C++并通过CGO…", "目录结构会随版本调整，阅读时要先切到与部署一致的v2.6.x标签，再从intern…"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：Milvus的源码在GitHub上，主要用Go语言写，搜索核心用C++并通过CGO…"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：目录结构会随版本调整，阅读时要先切到与部署一致的v2.6.x标签，再从intern…"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：目录结构会随版本调整，阅读时要先切到与部署一致的v2.6.x标签，再从intern…"

[[scenes]]
id = "s03"
narration_index = 3
title = "先看写入路径"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["先看写入路径", "Proxy接收insert请求后进入流式写入链路，WAL和Streaming No…", "具体函数和目录在小版本间可能变化，不能把某个旧文件路径当成永久API"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：先看写入路径"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：Proxy接收insert请求后进入流式写入链路，WAL和Streaming No…"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：具体函数和目录在小版本间可能变化，不能把某个旧文件路径当成永久API"

[[scenes]]
id = "s04"
narration_index = 4
title = "再看搜索路径"
purpose = "demo"
visual_type = "graph-search"
layout = "diagram"
key_points = ["再看搜索路径", "Proxy收到search请求后，从QueryCoord获取Segment分布，把…", "QueryNode在本地执行ANN搜索，代码在internal/querynode…"]
components = ["graph-layers", "search-route", "candidate-nodes"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "graph-layers"
description = "建立场景主题：再看搜索路径"

[[scenes.beats]]
at = 0.36
action = "traverse"
target = "search-route"
description = "用动态图解展开：Proxy收到search请求后，从QueryCoord获取Segment分布，把…"

[[scenes.beats]]
at = 0.72
action = "arrive"
target = "candidate-nodes"
description = "突出结论并承接下一段：QueryNode在本地执行ANN搜索，代码在internal/querynode…"

[[scenes]]
id = "s05"
narration_index = 5
title = "knowhere是Milvus的向量搜索引擎，独立仓库"
purpose = "demo"
visual_type = "graph-search"
layout = "diagram"
key_points = ["knowhere是Milvus的向量搜索引擎，独立仓库", "它封装了faiss、hnswlib等开源库，提供统一的索引接口", "如果你想理解HNSW搜索的具体实现，看knowhere/index/hnsw目录"]
components = ["graph-layers", "search-route", "candidate-nodes"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "graph-layers"
description = "建立场景主题：knowhere是Milvus的向量搜索引擎，独立仓库"

[[scenes.beats]]
at = 0.36
action = "traverse"
target = "search-route"
description = "用动态图解展开：它封装了faiss、hnswlib等开源库，提供统一的索引接口"

[[scenes.beats]]
at = 0.72
action = "arrive"
target = "candidate-nodes"
description = "突出结论并承接下一段：如果你想理解HNSW搜索的具体实现，看knowhere/index/hnsw目录"

[[scenes]]
id = "s06"
narration_index = 6
title = "Segment的生命周期管理在DataCoord里"
purpose = "demo"
visual_type = "architecture"
layout = "diagram"
key_points = ["Segment的生命周期管理在DataCoord里", "internal/datacoord/segment_manager.go管理Se…", "Compaction逻辑在internal/datacoord/compactio…"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：Segment的生命周期管理在DataCoord里"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：internal/datacoord/segment_manager.go管理Se…"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：Compaction逻辑在internal/datacoord/compactio…"

[[scenes]]
id = "s07"
narration_index = 7
title = "怎么高效阅读源码"
purpose = "demo"
visual_type = "architecture"
layout = "diagram"
key_points = ["怎么高效阅读源码", "几个建议", "第一，从接口入手：先看proto定义，理解每个RPC的输入输出"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：怎么高效阅读源码"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：几个建议"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：第一，从接口入手：先看proto定义，理解每个RPC的输入输出"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "读源码不是为了改源码，是为了理解黑盒", "知道写入走WAL、搜索走knowhere、Segment有生命周期，遇到问题时就能…"]
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
description = "用动态图解展开：读源码不是为了改源码，是为了理解黑盒"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：知道写入走WAL、搜索走knowhere、Segment有生命周期，遇到问题时就能…"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
