# Chapter 15 分区 Partition 设计视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/15-分区Partition设计.md`
- 核心问题：用可视化方式讲清《15 分区 Partition 设计》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "15"
title = "分区 Partition 设计"
source_doc = "../../milvus-master-course/docs/15-分区Partition设计.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "如果你的数据天然按某个维度分成几大块——比如按租户、按…"
purpose = "hook"
visual_type = "hook-comparison"
layout = "split"
key_points = ["上一章我们用标量过滤缩小搜索范围，但过滤是逻辑层面的", "如果你的数据天然按某个维度分成几大块——比如按租户、按时间、按类别——那物理隔离比…", "这就是Partition分区"]
components = ["question-card", "before-after-panels", "conflict-highlight"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "question-card"
description = "建立场景主题：上一章我们用标量过滤缩小搜索范围，但过滤是逻辑层面的"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "before-after-panels"
description = "用动态图解展开：如果你的数据天然按某个维度分成几大块——比如按租户、按时间、按类别——那物理隔离比…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "conflict-highlight"
description = "突出结论并承接下一段：这就是Partition分区"

[[scenes]]
id = "s02"
narration_index = 2
title = "Partition和Filter的区别是什么"
purpose = "comparison"
visual_type = "cluster-search"
layout = "diagram"
key_points = ["Partition和Filter的区别是什么", "Filter是搜索时临时筛选，每次都要扫描索引判断条件", "Partition是写入时就把数据物理分开，搜索时直接跳过不相关的分区，连索引都不…"]
components = ["clusters", "centroids", "query-node", "selected-regions"]

[[scenes.beats]]
at = 0.00
action = "cluster"
target = "clusters"
description = "建立场景主题：Partition和Filter的区别是什么"

[[scenes.beats]]
at = 0.36
action = "probe"
target = "centroids"
description = "用动态图解展开：Filter是搜索时临时筛选，每次都要扫描索引判断条件"

[[scenes.beats]]
at = 0.72
action = "select"
target = "query-node"
description = "突出结论并承接下一段：Partition是写入时就把数据物理分开，搜索时直接跳过不相关的分区，连索引都不…"

[[scenes]]
id = "s03"
narration_index = 3
title = "什么时候用Partition"
purpose = "concept"
visual_type = "cluster-search"
layout = "diagram"
key_points = ["什么时候用Partition", "三种典型场景", "按租户分区：每个客户的数据放一个分区，搜索时指定分区名，天然隔离"]
components = ["clusters", "centroids", "query-node", "selected-regions"]

[[scenes.beats]]
at = 0.00
action = "cluster"
target = "clusters"
description = "建立场景主题：什么时候用Partition"

[[scenes.beats]]
at = 0.36
action = "probe"
target = "centroids"
description = "用动态图解展开：三种典型场景"

[[scenes.beats]]
at = 0.72
action = "select"
target = "query-node"
description = "突出结论并承接下一段：按租户分区：每个客户的数据放一个分区，搜索时指定分区名，天然隔离"

[[scenes]]
id = "s04"
narration_index = 4
title = "Partition的限制要知道"
purpose = "concept"
visual_type = "cluster-search"
layout = "diagram"
key_points = ["Partition的限制要知道", "Milvus二点六默认每个Collection最多允许一千零二十四个分区，实际限制…", "分区内的数据共享同一套Schema和索引配置，分区也不能嵌套"]
components = ["clusters", "centroids", "query-node", "selected-regions"]

[[scenes.beats]]
at = 0.00
action = "cluster"
target = "clusters"
description = "建立场景主题：Partition的限制要知道"

[[scenes.beats]]
at = 0.36
action = "probe"
target = "centroids"
description = "用动态图解展开：Milvus二点六默认每个Collection最多允许一千零二十四个分区，实际限制…"

[[scenes.beats]]
at = 0.72
action = "select"
target = "query-node"
description = "突出结论并承接下一段：分区内的数据共享同一套Schema和索引配置，分区也不能嵌套"

[[scenes]]
id = "s05"
narration_index = 5
title = "在Milvus里怎么用"
purpose = "demo"
visual_type = "cluster-search"
layout = "diagram"
key_points = ["在Milvus里怎么用", "创建分区：client.create_partition(collection_n…", "写入时指定分区：client.upsert(collection_name, da…"]
components = ["clusters", "centroids", "query-node", "selected-regions"]

[[scenes.beats]]
at = 0.00
action = "cluster"
target = "clusters"
description = "建立场景主题：在Milvus里怎么用"

[[scenes.beats]]
at = 0.36
action = "probe"
target = "centroids"
description = "用动态图解展开：创建分区：client.create_partition(collection_n…"

[[scenes.beats]]
at = 0.72
action = "select"
target = "query-node"
description = "突出结论并承接下一段：写入时指定分区：client.upsert(collection_name, da…"

[[scenes]]
id = "s06"
narration_index = 6
title = "Partition Key是另一种方式"
purpose = "concept"
visual_type = "cluster-search"
layout = "diagram"
key_points = ["Partition Key是另一种方式", "不用手动管理分区，而是指定一个字段作为Partition Key，Milvus自动…", "好处是不用手动创建分区，坏处是分区数量和分布由Milvus控制，不够灵活"]
components = ["clusters", "centroids", "query-node", "selected-regions"]

[[scenes.beats]]
at = 0.00
action = "cluster"
target = "clusters"
description = "建立场景主题：Partition Key是另一种方式"

[[scenes.beats]]
at = 0.36
action = "probe"
target = "centroids"
description = "用动态图解展开：不用手动管理分区，而是指定一个字段作为Partition Key，Milvus自动…"

[[scenes.beats]]
at = 0.72
action = "select"
target = "query-node"
description = "突出结论并承接下一段：好处是不用手动创建分区，坏处是分区数量和分布由Milvus控制，不够灵活"

[[scenes]]
id = "s07"
narration_index = 7
title = "一个常见的设计模式是时间分区加TTL"
purpose = "concept"
visual_type = "cluster-search"
layout = "diagram"
key_points = ["一个常见的设计模式是时间分区加TTL", "按月创建分区，比如2024_01、2024_02", "数据写入对应月份的分区"]
components = ["clusters", "centroids", "query-node", "selected-regions"]

[[scenes.beats]]
at = 0.00
action = "cluster"
target = "clusters"
description = "建立场景主题：一个常见的设计模式是时间分区加TTL"

[[scenes.beats]]
at = 0.36
action = "probe"
target = "centroids"
description = "用动态图解展开：按月创建分区，比如2024_01、2024_02"

[[scenes.beats]]
at = 0.72
action = "select"
target = "query-node"
description = "突出结论并承接下一段：数据写入对应月份的分区"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "Partition是物理隔离，Filter是逻辑筛选", "数据天然分块且块数不多时用Partition，否则用Filter"]
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
description = "用动态图解展开：Partition是物理隔离，Filter是逻辑筛选"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：数据天然分块且块数不多时用Partition，否则用Filter"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
