# Chapter 35 海量数据架构设计视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/35-海量数据架构设计.md`
- 核心问题：用可视化方式讲清《35 海量数据架构设计》中的关键概念、工程流程与选择依据
- 场景数量：9 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "35"
title = "海量数据架构设计"
source_doc = "../../milvus-master-course/docs/35-海量数据架构设计.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "当数据量从百万级跳到亿级甚至十亿级，很多在小规模下不是…"
purpose = "hook"
visual_type = "hook-comparison"
layout = "split"
key_points = ["当数据量从百万级跳到亿级甚至十亿级，很多在小规模下不是问题的事情都变成了问题", "内存放不下、索引建不完、搜索延迟飙升、写入吞吐跟不上", "这一章我们聊海量数据场景下的架构设计：分片策略、冷热分层、索引选择、以及容量规划"]
components = ["question-card", "before-after-panels", "conflict-highlight"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "question-card"
description = "建立场景主题：当数据量从百万级跳到亿级甚至十亿级，很多在小规模下不是问题的事情都变成了问题"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "before-after-panels"
description = "用动态图解展开：内存放不下、索引建不完、搜索延迟飙升、写入吞吐跟不上"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "conflict-highlight"
description = "突出结论并承接下一段：这一章我们聊海量数据场景下的架构设计：分片策略、冷热分层、索引选择、以及容量规划"

[[scenes]]
id = "s02"
narration_index = 2
title = "第一个问题：内存放不下"
purpose = "concept"
visual_type = "graph-search"
layout = "diagram"
key_points = ["第一个问题：内存放不下", "一亿条768维向量，光原始数据就要300G", "加上HNSW索引的图结构，总共需要400G以上内存"]
components = ["graph-layers", "search-route", "candidate-nodes"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "graph-layers"
description = "建立场景主题：第一个问题：内存放不下"

[[scenes.beats]]
at = 0.36
action = "traverse"
target = "search-route"
description = "用动态图解展开：一亿条768维向量，光原始数据就要300G"

[[scenes.beats]]
at = 0.72
action = "arrive"
target = "candidate-nodes"
description = "突出结论并承接下一段：加上HNSW索引的图结构，总共需要400G以上内存"

[[scenes]]
id = "s03"
narration_index = 3
title = "分片策略"
purpose = "concept"
visual_type = "cluster-search"
layout = "diagram"
key_points = ["分片策略", "Milvus内部按Segment分片，但业务层面也需要考虑分片", "如果数据有天然的分区维度，比如按租户或按时间，用Partition物理隔离"]
components = ["clusters", "centroids", "query-node", "selected-regions"]

[[scenes.beats]]
at = 0.00
action = "cluster"
target = "clusters"
description = "建立场景主题：分片策略"

[[scenes.beats]]
at = 0.36
action = "probe"
target = "centroids"
description = "用动态图解展开：Milvus内部按Segment分片，但业务层面也需要考虑分片"

[[scenes.beats]]
at = 0.72
action = "select"
target = "query-node"
description = "突出结论并承接下一段：如果数据有天然的分区维度，比如按租户或按时间，用Partition物理隔离"

[[scenes]]
id = "s04"
narration_index = 4
title = "冷热分层是海量数据的标配"
purpose = "concept"
visual_type = "graph-search"
layout = "diagram"
key_points = ["冷热分层是海量数据的标配", "热数据是最近写入的、访问频率高的，放在内存里用HNSW索引，保证低延迟", "冷数据是历史数据、访问频率低的，用DISKANN索引放磁盘，或者直接release…"]
components = ["graph-layers", "search-route", "candidate-nodes"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "graph-layers"
description = "建立场景主题：冷热分层是海量数据的标配"

[[scenes.beats]]
at = 0.36
action = "traverse"
target = "search-route"
description = "用动态图解展开：热数据是最近写入的、访问频率高的，放在内存里用HNSW索引，保证低延迟"

[[scenes.beats]]
at = 0.72
action = "arrive"
target = "candidate-nodes"
description = "突出结论并承接下一段：冷数据是历史数据、访问频率低的，用DISKANN索引放磁盘，或者直接release…"

[[scenes]]
id = "s05"
narration_index = 5
title = "索引选择在海量场景下更关键"
purpose = "comparison"
visual_type = "graph-search"
layout = "diagram"
key_points = ["索引选择在海量场景下更关键", "一亿条以下用HNSW加多副本", "一亿到十亿用IVF_PQ或DISKANN"]
components = ["graph-layers", "search-route", "candidate-nodes"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "graph-layers"
description = "建立场景主题：索引选择在海量场景下更关键"

[[scenes.beats]]
at = 0.36
action = "traverse"
target = "search-route"
description = "用动态图解展开：一亿条以下用HNSW加多副本"

[[scenes.beats]]
at = 0.72
action = "arrive"
target = "candidate-nodes"
description = "突出结论并承接下一段：一亿到十亿用IVF_PQ或DISKANN"

[[scenes]]
id = "s06"
narration_index = 6
title = "容量规划怎么做"
purpose = "concept"
visual_type = "graph-search"
layout = "diagram"
key_points = ["容量规划怎么做", "先算内存需求：向量数乘以维度乘以4字节乘以索引系数", "HNSW系数约1.5，IVF_FLAT系数约1.1，IVF_PQ系数约0.1到0.3"]
components = ["graph-layers", "search-route", "candidate-nodes"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "graph-layers"
description = "建立场景主题：容量规划怎么做"

[[scenes.beats]]
at = 0.36
action = "traverse"
target = "search-route"
description = "用动态图解展开：先算内存需求：向量数乘以维度乘以4字节乘以索引系数"

[[scenes.beats]]
at = 0.72
action = "arrive"
target = "candidate-nodes"
description = "突出结论并承接下一段：HNSW系数约1.5，IVF_FLAT系数约1.1，IVF_PQ系数约0.1到0.3"

[[scenes]]
id = "s07"
narration_index = 7
title = "写入吞吐怎么扩展"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["写入吞吐怎么扩展", "先看瓶颈是在客户端、Proxy、WAL、Streaming Node还是对象存储", "集群可以扩展Streaming Node和流式存储分片，客户端也可以在限流下并发批…"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：写入吞吐怎么扩展"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：先看瓶颈是在客户端、Proxy、WAL、Streaming Node还是对象存储"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：集群可以扩展Streaming Node和流式存储分片，客户端也可以在限流下并发批…"

[[scenes]]
id = "s08"
narration_index = 8
title = "一个容量规划示例：十亿级商品向量可以按稳定的业务维度缩…"
purpose = "concept"
visual_type = "compression"
layout = "diagram"
key_points = ["一个容量规划示例：十亿级商品向量可以按稳定的业务维度缩小搜索范围，并评估IVF_P…", "QueryNode数量、内存规格、P99目标和Streaming Node数量不能…"]
components = ["source-vector", "segments", "codebook", "memory-bars"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "source-vector"
description = "建立场景主题：一个容量规划示例：十亿级商品向量可以按稳定的业务维度缩小搜索范围，并评估IVF_P…"

[[scenes.beats]]
at = 0.36
action = "encode"
target = "segments"
description = "用动态图解展开：QueryNode数量、内存规格、P99目标和Streaming Node数量不能…"

[[scenes.beats]]
at = 0.72
action = "compare"
target = "codebook"
description = "突出结论并承接下一段：QueryNode数量、内存规格、P99目标和Streaming Node数量不能…"

[[scenes]]
id = "s09"
narration_index = 9
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "海量数据架构的核心是：压缩减内存、分片减扫描、冷热分层减成本、水平扩展提吞吐", "没有银弹，每个选择都是trade-off"]
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
description = "用动态图解展开：海量数据架构的核心是：压缩减内存、分片减扫描、冷热分层减成本、水平扩展提吞吐"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：没有银弹，每个选择都是trade-off"
```

## 人工检查

- [x] 9 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
