# Chapter 11 HNSW 原理与实战视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/11-HNSW原理与实战.md`
- 核心问题：用可视化方式讲清《11 HNSW 原理与实战》中的关键概念、工程流程与选择依据
- 场景数量：9 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "11"
title = "HNSW 原理与实战"
source_doc = "../../milvus-master-course/docs/11-HNSW原理与实战.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "HNSW的核心思想完全不同：它不分区，而是建一个多层导…"
purpose = "hook"
visual_type = "learning-map"
layout = "full"
key_points = ["上一章我们学了IVF的分区搜索，这一章看HNSW——目前最流行的向量索引", "HNSW的核心思想完全不同：它不分区，而是建一个多层导航图", "我们搞清楚三件事：图怎么建、怎么搜、M和ef怎么调"]
components = ["chapter-map", "learning-goals", "progress-path"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "chapter-map"
description = "建立场景主题：上一章我们学了IVF的分区搜索，这一章看HNSW——目前最流行的向量索引"

[[scenes.beats]]
at = 0.36
action = "connect"
target = "learning-goals"
description = "用动态图解展开：HNSW的核心思想完全不同：它不分区，而是建一个多层导航图"

[[scenes.beats]]
at = 0.72
action = "preview"
target = "progress-path"
description = "突出结论并承接下一段：我们搞清楚三件事：图怎么建、怎么搜、M和ef怎么调"

[[scenes]]
id = "s02"
narration_index = 2
title = "HNSW的全称是Hierarchical Naviga…"
purpose = "concept"
visual_type = "graph-search"
layout = "diagram"
key_points = ["HNSW的全称是Hierarchical Navigable Small World", "想象一个多层地图：最上层只有几个大城市，中间层有区县，最底层有每条街道", "搜索时从最上层开始，几步跳到目标城市附近，然后逐层下沉，越来越精细，最终在底层找到…"]
components = ["graph-layers", "search-route", "candidate-nodes"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "graph-layers"
description = "建立场景主题：HNSW的全称是Hierarchical Navigable Small World"

[[scenes.beats]]
at = 0.36
action = "traverse"
target = "search-route"
description = "用动态图解展开：想象一个多层地图：最上层只有几个大城市，中间层有区县，最底层有每条街道"

[[scenes.beats]]
at = 0.72
action = "arrive"
target = "candidate-nodes"
description = "突出结论并承接下一段：搜索时从最上层开始，几步跳到目标城市附近，然后逐层下沉，越来越精细，最终在底层找到…"

[[scenes]]
id = "s03"
narration_index = 3
title = "构建过程是这样的"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["构建过程是这样的", "每插入一条向量，随机决定它出现在哪几层", "然后在每一层，把它和附近的节点连边"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：构建过程是这样的"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：每插入一条向量，随机决定它出现在哪几层"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：然后在每一层，把它和附近的节点连边"

[[scenes]]
id = "s04"
narration_index = 4
title = "搜索时从最上层的入口点开始，贪心地沿着边走向离查询最近…"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["搜索时从最上层的入口点开始，贪心地沿着边走向离查询最近的节点", "到了某一层走不动了，就下沉到下一层继续", "到了最底层，用一个优先队列维护候选集，参数ef决定队列大小"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：搜索时从最上层的入口点开始，贪心地沿着边走向离查询最近的节点"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：到了某一层走不动了，就下沉到下一层继续"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：到了最底层，用一个优先队列维护候选集，参数ef决定队列大小"

[[scenes]]
id = "s05"
narration_index = 5
title = "M怎么设"
purpose = "comparison"
visual_type = "dashboard"
layout = "dashboard"
key_points = ["M怎么设", "16到64可以作为常见候选范围，而不是固定答案", "M增大会增加每个节点的邻接边，通常改善图连通性和召回，同时提高图结构内存与构建成本"]
components = ["metric-cards", "trend-chart", "threshold-line", "tradeoff-control"]

[[scenes.beats]]
at = 0.00
action = "reveal"
target = "metric-cards"
description = "建立场景主题：M怎么设"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "trend-chart"
description = "用动态图解展开：16到64可以作为常见候选范围，而不是固定答案"

[[scenes.beats]]
at = 0.72
action = "balance"
target = "threshold-line"
description = "突出结论并承接下一段：M增大会增加每个节点的邻接边，通常改善图连通性和召回，同时提高图结构内存与构建成本"

[[scenes]]
id = "s06"
narration_index = 6
title = "ef怎么调"
purpose = "concept"
visual_type = "dashboard"
layout = "dashboard"
key_points = ["ef怎么调", "ef通常不能小于TopK", "可以从64、128、256这样的候选值逐步测试，观察召回率和延迟变化"]
components = ["metric-cards", "trend-chart", "threshold-line", "tradeoff-control"]

[[scenes.beats]]
at = 0.00
action = "reveal"
target = "metric-cards"
description = "建立场景主题：ef怎么调"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "trend-chart"
description = "用动态图解展开：ef通常不能小于TopK"

[[scenes.beats]]
at = 0.72
action = "balance"
target = "threshold-line"
description = "突出结论并承接下一段：可以从64、128、256这样的候选值逐步测试，观察召回率和延迟变化"

[[scenes]]
id = "s07"
narration_index = 7
title = "HNSW的内存开销怎么算"
purpose = "concept"
visual_type = "graph-search"
layout = "diagram"
key_points = ["HNSW的内存开销怎么算", "大约是：向量本身的大小，加上每个节点M乘以2乘以8字节的图结构", "一百万条768维向量，M等于16，内存大约是3G向量加0.24G图结构，总共3.2…"]
components = ["graph-layers", "search-route", "candidate-nodes"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "graph-layers"
description = "建立场景主题：HNSW的内存开销怎么算"

[[scenes.beats]]
at = 0.36
action = "traverse"
target = "search-route"
description = "用动态图解展开：大约是：向量本身的大小，加上每个节点M乘以2乘以8字节的图结构"

[[scenes.beats]]
at = 0.72
action = "arrive"
target = "candidate-nodes"
description = "突出结论并承接下一段：一百万条768维向量，M等于16，内存大约是3G向量加0.24G图结构，总共3.2…"

[[scenes]]
id = "s08"
narration_index = 8
title = "HNSW vs IVF怎么选"
purpose = "concept"
visual_type = "graph-search"
layout = "diagram"
key_points = ["HNSW vs IVF怎么选", "HNSW搜索快、召回高、不需要训练，但内存大", "IVF内存小、支持GPU加速，但需要训练且召回率依赖nprobe调参"]
components = ["graph-layers", "search-route", "candidate-nodes"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "graph-layers"
description = "建立场景主题：HNSW vs IVF怎么选"

[[scenes.beats]]
at = 0.36
action = "traverse"
target = "search-route"
description = "用动态图解展开：HNSW搜索快、召回高、不需要训练，但内存大"

[[scenes.beats]]
at = 0.72
action = "arrive"
target = "candidate-nodes"
description = "突出结论并承接下一段：IVF内存小、支持GPU加速，但需要训练且召回率依赖nprobe调参"

[[scenes]]
id = "s09"
narration_index = 9
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "HNSW是目前综合表现最好的索引：搜索快、召回高、不需要训练数据", "代价是内存"]
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
description = "用动态图解展开：HNSW是目前综合表现最好的索引：搜索快、召回高、不需要训练数据"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：代价是内存"
```

## 人工检查

- [x] 9 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
