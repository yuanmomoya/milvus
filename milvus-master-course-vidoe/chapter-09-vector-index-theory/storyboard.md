# Chapter 09 向量索引原理视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/09-向量索引原理.md`
- 核心问题：用可视化方式讲清《09 向量索引原理》中的关键概念、工程流程与选择依据
- 场景数量：9 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "09"
title = "向量索引原理"
source_doc = "../../milvus-master-course/docs/09-向量索引原理.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "但一亿条向量怎么快速搜索"
purpose = "hook"
visual_type = "learning-map"
layout = "full"
key_points = ["上一章我们选好了Embedding模型，向量有了", "但一亿条向量怎么快速搜索", "靠索引"]
components = ["chapter-map", "learning-goals", "progress-path"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "chapter-map"
description = "建立场景主题：上一章我们选好了Embedding模型，向量有了"

[[scenes.beats]]
at = 0.36
action = "connect"
target = "learning-goals"
description = "用动态图解展开：但一亿条向量怎么快速搜索"

[[scenes.beats]]
at = 0.72
action = "preview"
target = "progress-path"
description = "突出结论并承接下一段：靠索引"

[[scenes]]
id = "s02"
narration_index = 2
title = "索引的本质"
purpose = "concept"
visual_type = "dashboard"
layout = "dashboard"
key_points = ["索引的本质", "暴力搜索是O(N)，一百万条向量每次查询要计算一百万次距离，实际延迟取决于维度、硬…", "ANN索引的目标是只访问一部分候选数据，换取更低延迟"]
components = ["metric-cards", "trend-chart", "threshold-line", "tradeoff-control"]

[[scenes.beats]]
at = 0.00
action = "reveal"
target = "metric-cards"
description = "建立场景主题：索引的本质"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "trend-chart"
description = "用动态图解展开：暴力搜索是O(N)，一百万条向量每次查询要计算一百万次距离，实际延迟取决于维度、硬…"

[[scenes.beats]]
at = 0.72
action = "balance"
target = "threshold-line"
description = "突出结论并承接下一段：ANN索引的目标是只访问一部分候选数据，换取更低延迟"

[[scenes]]
id = "s03"
narration_index = 3
title = "FLAT不是真正的索引，它就是暴力扫描"
purpose = "concept"
visual_type = "dashboard"
layout = "dashboard"
key_points = ["FLAT不是真正的索引，它就是暴力扫描", "优点是召回率100%，缺点是慢", "适合数据量小于十万的场景，或者作为评测基准"]
components = ["metric-cards", "trend-chart", "threshold-line", "tradeoff-control"]

[[scenes.beats]]
at = 0.00
action = "reveal"
target = "metric-cards"
description = "建立场景主题：FLAT不是真正的索引，它就是暴力扫描"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "trend-chart"
description = "用动态图解展开：优点是召回率100%，缺点是慢"

[[scenes.beats]]
at = 0.72
action = "balance"
target = "threshold-line"
description = "突出结论并承接下一段：适合数据量小于十万的场景，或者作为评测基准"

[[scenes]]
id = "s04"
narration_index = 4
title = "IVF的思路是分片区"
purpose = "concept"
visual_type = "cluster-search"
layout = "diagram"
key_points = ["IVF的思路是分片区", "先用KMeans把所有向量聚成nlist个簇，每个簇有一个中心点", "搜索时先找离查询最近的nprobe个中心，然后只扫描这几个簇里的向量"]
components = ["clusters", "centroids", "query-node", "selected-regions"]

[[scenes.beats]]
at = 0.00
action = "cluster"
target = "clusters"
description = "建立场景主题：IVF的思路是分片区"

[[scenes.beats]]
at = 0.36
action = "probe"
target = "centroids"
description = "用动态图解展开：先用KMeans把所有向量聚成nlist个簇，每个簇有一个中心点"

[[scenes.beats]]
at = 0.72
action = "select"
target = "query-node"
description = "突出结论并承接下一段：搜索时先找离查询最近的nprobe个中心，然后只扫描这几个簇里的向量"

[[scenes]]
id = "s05"
narration_index = 5
title = "HNSW的思路是修高速公路"
purpose = "concept"
visual_type = "graph-search"
layout = "diagram"
key_points = ["HNSW的思路是修高速公路", "它建一个多层图：最上层节点稀疏，几步就能跳到目标附近", "逐层下沉，节点越来越密，搜索越来越精细"]
components = ["graph-layers", "search-route", "candidate-nodes"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "graph-layers"
description = "建立场景主题：HNSW的思路是修高速公路"

[[scenes.beats]]
at = 0.36
action = "traverse"
target = "search-route"
description = "用动态图解展开：它建一个多层图：最上层节点稀疏，几步就能跳到目标附近"

[[scenes.beats]]
at = 0.72
action = "arrive"
target = "candidate-nodes"
description = "突出结论并承接下一段：逐层下沉，节点越来越密，搜索越来越精细"

[[scenes]]
id = "s06"
narration_index = 6
title = "PQ是压缩大师"
purpose = "concept"
visual_type = "compression"
layout = "diagram"
key_points = ["PQ是压缩大师", "它把一个长向量切成若干子段，每段用一个短编码代替", "搜索时用近似距离快速筛选候选集，再用原始向量精排"]
components = ["source-vector", "segments", "codebook", "memory-bars"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "source-vector"
description = "建立场景主题：PQ是压缩大师"

[[scenes.beats]]
at = 0.36
action = "encode"
target = "segments"
description = "用动态图解展开：它把一个长向量切成若干子段，每段用一个短编码代替"

[[scenes.beats]]
at = 0.72
action = "compare"
target = "codebook"
description = "突出结论并承接下一段：搜索时用近似距离快速筛选候选集，再用原始向量精排"

[[scenes]]
id = "s07"
narration_index = 7
title = "DISKANN是磁盘索引"
purpose = "concept"
visual_type = "graph-search"
layout = "diagram"
key_points = ["DISKANN是磁盘索引", "当数据量大到内存放不下时，把图索引存在磁盘上，搜索时按需加载", "延迟比纯内存索引高，但能处理十亿级数据"]
components = ["graph-layers", "search-route", "candidate-nodes"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "graph-layers"
description = "建立场景主题：DISKANN是磁盘索引"

[[scenes.beats]]
at = 0.36
action = "traverse"
target = "search-route"
description = "用动态图解展开：当数据量大到内存放不下时，把图索引存在磁盘上，搜索时按需加载"

[[scenes.beats]]
at = 0.72
action = "arrive"
target = "candidate-nodes"
description = "突出结论并承接下一段：延迟比纯内存索引高，但能处理十亿级数据"

[[scenes]]
id = "s08"
narration_index = 8
title = "怎么选"
purpose = "concept"
visual_type = "graph-search"
layout = "diagram"
key_points = ["怎么选", "看三个维度：数据量、内存预算、延迟要求", "十万以下用FLAT"]
components = ["graph-layers", "search-route", "candidate-nodes"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "graph-layers"
description = "建立场景主题：怎么选"

[[scenes.beats]]
at = 0.36
action = "traverse"
target = "search-route"
description = "用动态图解展开：看三个维度：数据量、内存预算、延迟要求"

[[scenes.beats]]
at = 0.72
action = "arrive"
target = "candidate-nodes"
description = "突出结论并承接下一段：十万以下用FLAT"

[[scenes]]
id = "s09"
narration_index = 9
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "索引的本质是用召回率换速度", "五种索引各有适用场景，没有万能选择"]
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
description = "用动态图解展开：索引的本质是用召回率换速度"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：五种索引各有适用场景，没有万能选择"
```

## 人工检查

- [x] 9 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
