# Chapter 02 Milvus整体架构视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/02-Milvus整体架构.md`
- 核心问题：用可视化方式讲清《02 Milvus整体架构》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "02"
title = "Milvus整体架构"
source_doc = "../../milvus-master-course/docs/02-Milvus整体架构.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "这一章我们搞清楚Milvus的整体架构：它是怎么把向量…"
purpose = "hook"
visual_type = "hook-comparison"
layout = "split"
key_points = ["上一章我们知道了向量检索的原理，但原理只是一半，工程落地才是另一半", "这一章我们搞清楚Milvus的整体架构：它是怎么把向量写入、索引构建和搜索这三件事…", "理解了架构，后面排查问题就有方向了"]
components = ["question-card", "before-after-panels", "conflict-highlight"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "question-card"
description = "建立场景主题：上一章我们知道了向量检索的原理，但原理只是一半，工程落地才是另一半"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "before-after-panels"
description = "用动态图解展开：这一章我们搞清楚Milvus的整体架构：它是怎么把向量写入、索引构建和搜索这三件事…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "conflict-highlight"
description = "突出结论并承接下一段：理解了架构，后面排查问题就有方向了"

[[scenes]]
id = "s02"
narration_index = 2
title = "先用一个类比建立直觉"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["先用一个类比建立直觉", "Milvus的架构像一个大型物流中心", "Proxy是前台接待，负责接收客户订单"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：先用一个类比建立直觉"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：Milvus的架构像一个大型物流中心"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：Proxy是前台接待，负责接收客户订单"

[[scenes]]
id = "s03"
narration_index = 3
title = "以Milvus二点六为准，协调层主要包括RootCoo…"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["以Milvus二点六为准，协调层主要包括RootCoord、DataCoord和Q…", "RootCoord管元数据，DataCoord管Segment和数据任务，Quer…", "执行层包括Streaming Node、QueryNode和IndexNode，分…"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：以Milvus二点六为准，协调层主要包括RootCoord、DataCoord和Q…"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：RootCoord管元数据，DataCoord管Segment和数据任务，Quer…"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：执行层包括Streaming Node、QueryNode和IndexNode，分…"

[[scenes]]
id = "s04"
narration_index = 4
title = "知道了组件分工，来看数据怎么写进去"
purpose = "demo"
visual_type = "architecture"
layout = "diagram"
key_points = ["知道了组件分工，来看数据怎么写进去", "应用调用insert，Proxy把写入交给流式写入链路并进入WAL", "达到相应一致性要求后客户端收到成功响应"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：知道了组件分工，来看数据怎么写进去"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：应用调用insert，Proxy把写入交给流式写入链路并进入WAL"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：达到相应一致性要求后客户端收到成功响应"

[[scenes]]
id = "s05"
narration_index = 5
title = "光写入还不够，还得能搜出来"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["光写入还不够，还得能搜出来", "查询时Proxy把请求拆给多个QueryNode，每个Node搜自己负责的segm…", "Proxy再把所有局部结果归并排序，得到全局TopK返回给客户端"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：光写入还不够，还得能搜出来"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：查询时Proxy把请求拆给多个QueryNode，每个Node搜自己负责的segm…"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：Proxy再把所有局部结果归并排序，得到全局TopK返回给客户端"

[[scenes]]
id = "s06"
narration_index = 6
title = "这里有个关键概念：Segment"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["这里有个关键概念：Segment", "它是Milvus数据管理的最小单位", "新写入的数据先在growing segment里，flush后变成sealed s…"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：这里有个关键概念：Segment"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：它是Milvus数据管理的最小单位"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：新写入的数据先在growing segment里，flush后变成sealed s…"

[[scenes]]
id = "s07"
narration_index = 7
title = "说说Standalone和Cluster的区别"
purpose = "demo"
visual_type = "architecture"
layout = "diagram"
key_points = ["最后说说Standalone和Cluster的区别", "Standalone把协调与执行组件合并在单个Milvus进程中，并使用内置的流式…", "Cluster模式把组件拆成可独立部署和扩缩容的服务，适合需要高可用或更大规模的生…"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：最后说说Standalone和Cluster的区别"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：Standalone把协调与执行组件合并在单个Milvus进程中，并使用内置的流式…"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：Cluster模式把组件拆成可独立部署和扩缩容的服务，适合需要高可用或更大规模的生…"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "Milvus的核心是两条链路：写入链路把数据变成segment和索引，查询链路把分…", "后面所有调优都围绕这两条链路展开"]
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
description = "用动态图解展开：Milvus的核心是两条链路：写入链路把数据变成segment和索引，查询链路把分…"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：后面所有调优都围绕这两条链路展开"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
