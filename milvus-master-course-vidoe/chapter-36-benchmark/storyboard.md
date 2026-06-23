# Chapter 36 性能压测与 Benchmark视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/36-性能压测与Benchmark.md`
- 核心问题：用可视化方式讲清《36 性能压测与 Benchmark》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "36"
title = "性能压测与 Benchmark"
source_doc = "../../milvus-master-course/docs/36-性能压测与Benchmark.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "前面我们做了很多优化决策：选HNSW还是IVF、M设1…"
purpose = "hook"
visual_type = "learning-map"
layout = "full"
key_points = ["前面我们做了很多优化决策：选HNSW还是IVF、M设16还是32、nprobe设多少", "但这些决策不能靠猜，要靠数据说话", "这一章我们做性能压测：用Benchmark量化不同配置下的QPS、延迟和召回率，找…"]
components = ["chapter-map", "learning-goals", "progress-path"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "chapter-map"
description = "建立场景主题：前面我们做了很多优化决策：选HNSW还是IVF、M设16还是32、nprobe设多少"

[[scenes.beats]]
at = 0.36
action = "connect"
target = "learning-goals"
description = "用动态图解展开：但这些决策不能靠猜，要靠数据说话"

[[scenes.beats]]
at = 0.72
action = "preview"
target = "progress-path"
description = "突出结论并承接下一段：这一章我们做性能压测：用Benchmark量化不同配置下的QPS、延迟和召回率，找…"

[[scenes]]
id = "s02"
narration_index = 2
title = "Benchmark要测什么"
purpose = "concept"
visual_type = "dashboard"
layout = "dashboard"
key_points = ["Benchmark要测什么", "三个核心指标", "QPS：每秒能处理多少搜索请求，衡量吞吐能力"]
components = ["metric-cards", "trend-chart", "threshold-line", "tradeoff-control"]

[[scenes.beats]]
at = 0.00
action = "reveal"
target = "metric-cards"
description = "建立场景主题：Benchmark要测什么"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "trend-chart"
description = "用动态图解展开：三个核心指标"

[[scenes.beats]]
at = 0.72
action = "balance"
target = "threshold-line"
description = "突出结论并承接下一段：QPS：每秒能处理多少搜索请求，衡量吞吐能力"

[[scenes]]
id = "s03"
narration_index = 3
title = "测试方法"
purpose = "comparison"
visual_type = "dashboard"
layout = "dashboard"
key_points = ["测试方法", "准备一个数据集，比如十万或一百万条随机向量", "先用FLAT索引做暴力搜索，得到每个查询的精确TopK作为ground truth"]
components = ["metric-cards", "trend-chart", "threshold-line", "tradeoff-control"]

[[scenes.beats]]
at = 0.00
action = "reveal"
target = "metric-cards"
description = "建立场景主题：测试方法"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "trend-chart"
description = "用动态图解展开：准备一个数据集，比如十万或一百万条随机向量"

[[scenes.beats]]
at = 0.72
action = "balance"
target = "threshold-line"
description = "突出结论并承接下一段：先用FLAT索引做暴力搜索，得到每个查询的精确TopK作为ground truth"

[[scenes]]
id = "s04"
narration_index = 4
title = "项目里的benchmark脚本怎么用"
purpose = "demo"
visual_type = "code-terminal"
layout = "code"
key_points = ["项目里的benchmark脚本怎么用", "cd到demos/benchmark目录，运行python benchmark.py", "参数包括：rows数据量、dim维度、index索引类型、concurrency并…"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：项目里的benchmark脚本怎么用"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：cd到demos/benchmark目录，运行python benchmark.py"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：参数包括：rows数据量、dim维度、index索引类型、concurrency并…"

[[scenes]]
id = "s05"
narration_index = 5
title = "几个典型的对比实验"
purpose = "comparison"
visual_type = "graph-search"
layout = "diagram"
key_points = ["几个典型的对比实验", "实验一：HNSW的M从8到64，观察内存、QPS和召回率的变化", "实验二：IVF的nprobe从1到128，观察延迟和召回率的trade-off曲线"]
components = ["graph-layers", "search-route", "candidate-nodes"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "graph-layers"
description = "建立场景主题：几个典型的对比实验"

[[scenes.beats]]
at = 0.36
action = "traverse"
target = "search-route"
description = "用动态图解展开：实验一：HNSW的M从8到64，观察内存、QPS和召回率的变化"

[[scenes.beats]]
at = 0.72
action = "arrive"
target = "candidate-nodes"
description = "突出结论并承接下一段：实验二：IVF的nprobe从1到128，观察延迟和召回率的trade-off曲线"

[[scenes]]
id = "s06"
narration_index = 6
title = "怎么解读结果"
purpose = "concept"
visual_type = "dashboard"
layout = "dashboard"
key_points = ["怎么解读结果", "画两张图", "第一张：召回率-延迟曲线，横轴延迟纵轴召回率，找到拐点"]
components = ["metric-cards", "trend-chart", "threshold-line", "tradeoff-control"]

[[scenes.beats]]
at = 0.00
action = "reveal"
target = "metric-cards"
description = "建立场景主题：怎么解读结果"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "trend-chart"
description = "用动态图解展开：画两张图"

[[scenes.beats]]
at = 0.72
action = "balance"
target = "threshold-line"
description = "突出结论并承接下一段：第一张：召回率-延迟曲线，横轴延迟纵轴召回率，找到拐点"

[[scenes]]
id = "s07"
narration_index = 7
title = "生产环境的压测注意事项"
purpose = "concept"
visual_type = "cluster-search"
layout = "diagram"
key_points = ["生产环境的压测注意事项", "第一，用真实数据分布，不要用纯随机向量——真实数据的聚类特性会影响索引效果", "第二，测试时要预热，前几百个请求的延迟不准确"]
components = ["clusters", "centroids", "query-node", "selected-regions"]

[[scenes.beats]]
at = 0.00
action = "cluster"
target = "clusters"
description = "建立场景主题：生产环境的压测注意事项"

[[scenes.beats]]
at = 0.36
action = "probe"
target = "centroids"
description = "用动态图解展开：第一，用真实数据分布，不要用纯随机向量——真实数据的聚类特性会影响索引效果"

[[scenes.beats]]
at = 0.72
action = "select"
target = "query-node"
description = "突出结论并承接下一段：第二，测试时要预热，前几百个请求的延迟不准确"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "Benchmark是参数调优的科学方法", "不要猜，要测"]
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
description = "用动态图解展开：Benchmark是参数调优的科学方法"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：不要猜，要测"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
