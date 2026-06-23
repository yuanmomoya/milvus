# Chapter 17 查询性能调优视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/17-查询性能调优.md`
- 核心问题：用可视化方式讲清《17 查询性能调优》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "17"
title = "查询性能调优"
source_doc = "../../milvus-master-course/docs/17-查询性能调优.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "查询慢是生产环境最常见的问题"
purpose = "hook"
visual_type = "hook-comparison"
layout = "split"
key_points = ["上一章我们优化了写入，这一章优化搜索", "查询慢是生产环境最常见的问题", "要调优，首先得知道延迟花在哪里"]
components = ["question-card", "before-after-panels", "conflict-highlight"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "question-card"
description = "建立场景主题：上一章我们优化了写入，这一章优化搜索"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "before-after-panels"
description = "用动态图解展开：查询慢是生产环境最常见的问题"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "conflict-highlight"
description = "突出结论并承接下一段：要调优，首先得知道延迟花在哪里"

[[scenes]]
id = "s02"
narration_index = 2
title = "ANN搜索通常是核心耗时之一"
purpose = "comparison"
visual_type = "graph-search"
layout = "diagram"
key_points = ["ANN搜索通常是核心耗时之一", "HNSW的ef会影响召回和速度，IVF的nprobe也有类似权衡", "参数增大后究竟提升多少召回、增加多少延迟取决于数据和硬件"]
components = ["graph-layers", "search-route", "candidate-nodes"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "graph-layers"
description = "建立场景主题：ANN搜索通常是核心耗时之一"

[[scenes.beats]]
at = 0.36
action = "traverse"
target = "search-route"
description = "用动态图解展开：HNSW的ef会影响召回和速度，IVF的nprobe也有类似权衡"

[[scenes.beats]]
at = 0.72
action = "arrive"
target = "candidate-nodes"
description = "突出结论并承接下一段：参数增大后究竟提升多少召回、增加多少延迟取决于数据和硬件"

[[scenes]]
id = "s03"
narration_index = 3
title = "标量过滤的开销容易被忽视"
purpose = "concept"
visual_type = "metric-comparison"
layout = "split"
key_points = ["标量过滤的开销容易被忽视", "如果过滤字段没建索引，每次搜索都要全量扫描标量数据", "解决方案很简单：给高频过滤字段建INVERTED索引"]
components = ["comparison-cards", "tradeoff-axis", "decision-marker"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "comparison-cards"
description = "建立场景主题：标量过滤的开销容易被忽视"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "tradeoff-axis"
description = "用动态图解展开：如果过滤字段没建索引，每次搜索都要全量扫描标量数据"

[[scenes.beats]]
at = 0.72
action = "decide"
target = "decision-marker"
description = "突出结论并承接下一段：解决方案很简单：给高频过滤字段建INVERTED索引"

[[scenes]]
id = "s04"
narration_index = 4
title = "output_fields也会影响延迟"
purpose = "concept"
visual_type = "dashboard"
layout = "dashboard"
key_points = ["output_fields也会影响延迟", "搜索时指定返回哪些字段，Milvus需要从存储里读取这些字段的值", "如果返回一个4096字符的text字段，IO开销不小"]
components = ["metric-cards", "trend-chart", "threshold-line", "tradeoff-control"]

[[scenes.beats]]
at = 0.00
action = "reveal"
target = "metric-cards"
description = "建立场景主题：output_fields也会影响延迟"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "trend-chart"
description = "用动态图解展开：搜索时指定返回哪些字段，Milvus需要从存储里读取这些字段的值"

[[scenes.beats]]
at = 0.72
action = "balance"
target = "threshold-line"
description = "突出结论并承接下一段：如果返回一个4096字符的text字段，IO开销不小"

[[scenes]]
id = "s05"
narration_index = 5
title = "Segment数量是另一个隐藏杀手"
purpose = "concept"
visual_type = "metric-comparison"
layout = "split"
key_points = ["Segment数量是另一个隐藏杀手", "每个Segment都要独立搜索，结果再合并", "如果一个Collection有几千个小Segment，合并开销就很大"]
components = ["comparison-cards", "tradeoff-axis", "decision-marker"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "comparison-cards"
description = "建立场景主题：Segment数量是另一个隐藏杀手"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "tradeoff-axis"
description = "用动态图解展开：每个Segment都要独立搜索，结果再合并"

[[scenes.beats]]
at = 0.72
action = "decide"
target = "decision-marker"
description = "突出结论并承接下一段：如果一个Collection有几千个小Segment，合并开销就很大"

[[scenes]]
id = "s06"
narration_index = 6
title = "TopK的大小也影响性能"
purpose = "concept"
visual_type = "dashboard"
layout = "dashboard"
key_points = ["TopK的大小也影响性能", "TopK从10增大到1000，延迟可能翻几倍，因为需要维护更大的候选集", "如果业务只需要前10个结果，就不要设TopK等于100\"以防万一\""]
components = ["metric-cards", "trend-chart", "threshold-line", "tradeoff-control"]

[[scenes.beats]]
at = 0.00
action = "reveal"
target = "metric-cards"
description = "建立场景主题：TopK的大小也影响性能"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "trend-chart"
description = "用动态图解展开：TopK从10增大到1000，延迟可能翻几倍，因为需要维护更大的候选集"

[[scenes.beats]]
at = 0.72
action = "balance"
target = "threshold-line"
description = "突出结论并承接下一段：如果业务只需要前10个结果，就不要设TopK等于100\"以防万一\""

[[scenes]]
id = "s07"
narration_index = 7
title = "并发也是个维度"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["并发也是个维度", "单个搜索请求的延迟和并发请求数有关", "QPS上去后，QueryNode的CPU和内存压力增大，单次延迟会上升"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：并发也是个维度"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：单个搜索请求的延迟和并发请求数有关"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：QPS上去后，QueryNode的CPU和内存压力增大，单次延迟会上升"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "查询调优的思路是：定位瓶颈、逐个击破", "ANN参数找拐点、过滤字段建索引、output_fields精简、Segment合…"]
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
description = "用动态图解展开：查询调优的思路是：定位瓶颈、逐个击破"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：ANN参数找拐点、过滤字段建索引、output_fields精简、Segment合…"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
