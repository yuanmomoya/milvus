# Chapter 18 Milvus 集群部署视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/18-Milvus集群部署.md`
- 核心问题：用可视化方式讲清《18 Milvus 集群部署》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "18"
title = "Milvus 集群部署"
source_doc = "../../milvus-master-course/docs/18-Milvus集群部署.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "前面十七章我们一直在单机Standalone模式下工作"
purpose = "hook"
visual_type = "learning-map"
layout = "full"
key_points = ["前面十七章我们一直在单机Standalone模式下工作", "单机有天花板：CPU、内存、磁盘IO都是硬上限", "当数据量超过单机容量、写入吞吐需要水平扩展、或者需要高可用时，就该上集群了"]
components = ["chapter-map", "learning-goals", "progress-path"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "chapter-map"
description = "建立场景主题：前面十七章我们一直在单机Standalone模式下工作"

[[scenes.beats]]
at = 0.36
action = "connect"
target = "learning-goals"
description = "用动态图解展开：单机有天花板：CPU、内存、磁盘IO都是硬上限"

[[scenes.beats]]
at = 0.72
action = "preview"
target = "progress-path"
description = "突出结论并承接下一段：当数据量超过单机容量、写入吞吐需要水平扩展、或者需要高可用时，就该上集群了"

[[scenes]]
id = "s02"
narration_index = 2
title = "集群模式和Standalone的核心区别是：组件可以拆…"
purpose = "comparison"
visual_type = "architecture"
layout = "diagram"
key_points = ["集群模式和Standalone的核心区别是：组件可以拆分部署和独立扩缩容", "Proxy可以有多个，做负载均衡", "Streaming Node可以扩展流式写入能力，QueryNode分担搜索压力…"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：集群模式和Standalone的核心区别是：组件可以拆分部署和独立扩缩容"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：Proxy可以有多个，做负载均衡"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：Streaming Node可以扩展流式写入能力，QueryNode分担搜索压力…"

[[scenes]]
id = "s03"
narration_index = 3
title = "基础设施也不一样"
purpose = "demo"
visual_type = "architecture"
layout = "diagram"
key_points = ["基础设施也不一样", "Standalone使用内置流式存储，集群模式需要可靠的WAL或流式存储，具体实现…", "etcd与对象存储仍需要独立保障高可用"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：基础设施也不一样"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：Standalone使用内置流式存储，集群模式需要可靠的WAL或流式存储，具体实现…"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：etcd与对象存储仍需要独立保障高可用"

[[scenes]]
id = "s04"
narration_index = 4
title = "部署方式有三种"
purpose = "concept"
visual_type = "code-terminal"
layout = "code"
key_points = ["部署方式有三种", "Helm Chart部署到Kubernetes，这是生产推荐方式", "Docker Compose部署，适合测试和开发"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：部署方式有三种"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：Helm Chart部署到Kubernetes，这是生产推荐方式"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：Docker Compose部署，适合测试和开发"

[[scenes]]
id = "s05"
narration_index = 5
title = "扩容的思路是按瓶颈扩"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["扩容的思路是按瓶颈扩", "搜索资源不足时评估QueryNode，流式写入受限时检查WAL和Streaming…", "每种组件的资源模型不同，必须先看监控再扩容，不能把“慢”直接等同于“节点少”"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：扩容的思路是按瓶颈扩"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：搜索资源不足时评估QueryNode，流式写入受限时检查WAL和Streaming…"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：每种组件的资源模型不同，必须先看监控再扩容，不能把“慢”直接等同于“节点少”"

[[scenes]]
id = "s06"
narration_index = 6
title = "集群部署后，数据怎么分布"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["集群部署后，数据怎么分布", "Milvus用Segment作为调度单位", "QueryCoord负责把Segment分配给不同的QueryNode"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：集群部署后，数据怎么分布"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：Milvus用Segment作为调度单位"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：QueryCoord负责把Segment分配给不同的QueryNode"

[[scenes]]
id = "s07"
narration_index = 7
title = "有个重要概念：副本"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["有个重要概念：副本", "一个Collection可以加载多个副本，每个副本是完整数据的一份拷贝，分布在不同…", "副本数越多，搜索吞吐越高，但内存消耗也成倍增长"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：有个重要概念：副本"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：一个Collection可以加载多个副本，每个副本是完整数据的一份拷贝，分布在不同…"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：副本数越多，搜索吞吐越高，但内存消耗也成倍增长"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "集群部署的核心是：组件独立扩缩容、按瓶颈加资源、用副本提升吞吐", "从Standalone到Cluster不需要改应用代码，只需要改部署配置"]
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
description = "用动态图解展开：集群部署的核心是：组件独立扩缩容、按瓶颈加资源、用副本提升吞吐"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：从Standalone到Cluster不需要改应用代码，只需要改部署配置"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
