# Chapter 01 向量数据库基础视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/01-向量数据库基础.md`
- 目标受众：第一次接触向量数据库的 Python、AI 应用和后端开发者
- 核心问题：计算机如何理解“相似”，以及如何在海量向量中快速找到 TopK
- 学完能够：解释向量与 Embedding，区分三种距离度量，说清 HNSW、IVF、PQ 的直觉，
  并理解召回、延迟、吞吐与成本之间的权衡

## 视觉叙事

整章从“轿车和香蕉，哪个更像卡车”这个无歧义问题出发，逐步把自然语言映射为向量空间，
再把“相似”拆成距离计算，最后进入海量数据下的索引加速。画面应持续展示关系和过程，
不能退化为旁白句子的卡片列表。

## 分镜数据

```toml
schema_version = 1
chapter = "01"
title = "向量数据库基础"
source_doc = "../../milvus-master-course/docs/01-向量数据库基础.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "轿车、香蕉与卡车"
purpose = "hook"
visual_type = "hook-comparison"
layout = "split"
key_points = ["字段匹配不会自动理解语义", "向量检索计算相似关系", "本章：表示、距离、索引"]
components = ["query-card", "vehicle-nodes", "database-comparison", "learning-map"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "query-card"
description = "显示问题：轿车和香蕉，哪个更像卡车"

[[scenes.beats]]
at = 0.22
action = "compare"
target = "database-comparison"
description = "左侧传统数据库返回无法精确匹配，右侧向量数据库开始计算相似关系"

[[scenes.beats]]
at = 0.48
action = "connect"
target = "vehicle-nodes"
description = "轿车与卡车形成较强连线，香蕉与卡车形成较弱连线"

[[scenes.beats]]
at = 0.72
action = "reveal"
target = "learning-map"
description = "依次出现向量、距离、索引三项学习目标"

[[scenes]]
id = "s02"
narration_index = 2
title = "从货架编号到语义空间"
purpose = "comparison"
visual_type = "hook-comparison"
layout = "split"
key_points = ["传统数据库：精确条件", "向量数据库：语义邻近"]
components = ["library-shelves", "semantic-warehouse", "search-cursor"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "library-shelves"
description = "左侧显示按编号排列的图书货架，搜索光标只命中完全一致的编号"

[[scenes.beats]]
at = 0.35
action = "morph"
target = "semantic-warehouse"
description = "货架转换为按语义聚集的物品空间，相似物品自然靠近"

[[scenes.beats]]
at = 0.70
action = "highlight"
target = "semantic-neighbors"
description = "突出查询附近的相似对象，并显示 TopK 标签"

[[scenes]]
id = "s03"
narration_index = 3
title = "Embedding 是坐标测量仪"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["原始内容 → Embedding → 高维向量", "同一模型定义同一坐标系", "语义越近，空间距离越近"]
components = ["content-cards", "embedding-machine", "vector-values", "vector-space"]

[[scenes.beats]]
at = 0.00
action = "flow"
target = "content-cards"
description = "文字和图片卡片进入 Embedding 模型"

[[scenes.beats]]
at = 0.28
action = "transform"
target = "vector-values"
description = "内容转换为浮点数向量，保留少量数字示意"

[[scenes.beats]]
at = 0.55
action = "scatter"
target = "vector-space"
description = "向量落入二维投影视图，水果、交通工具等类别形成不同簇"

[[scenes.beats]]
at = 0.82
action = "highlight"
target = "semantic-neighbors"
description = "高亮语义相近的两个点及其短距离"

[[scenes]]
id = "s04"
narration_index = 4
title = "三种方式定义相似"
purpose = "comparison"
visual_type = "metric-comparison"
layout = "diagram"
key_points = ["COSINE 看方向", "L2 看直线距离", "IP 同时受方向和长度影响"]
components = ["metric-tabs", "vector-arrows", "distance-line", "score-cards"]

[[scenes.beats]]
at = 0.00
action = "draw"
target = "vector-arrows"
description = "绘制两组方向接近但长度不同的箭头"

[[scenes.beats]]
at = 0.25
action = "measure"
target = "cosine-angle"
description = "显示夹角缩小并突出 COSINE 分数升高"

[[scenes.beats]]
at = 0.50
action = "measure"
target = "distance-line"
description = "切换到两个点并绘制 L2 直线距离"

[[scenes.beats]]
at = 0.75
action = "compare"
target = "score-cards"
description = "并排展示 COSINE、L2、IP 的直觉和分数方向"

[[scenes]]
id = "s05"
narration_index = 5
title = "一亿次距离计算"
purpose = "problem"
visual_type = "dashboard"
layout = "split"
key_points = ["FLAT 扫描全部向量", "数据规模增长，计算成本线性增长", "需要 ANN 缩小候选集"]
components = ["scale-counter", "vector-grid", "scan-beam", "latency-meter"]

[[scenes.beats]]
at = 0.00
action = "scan"
target = "vector-grid"
description = "查询光束逐个扫描一百个向量点"

[[scenes.beats]]
at = 0.30
action = "count"
target = "scale-counter"
description = "数据量从一百快速增长到一百万、一亿"

[[scenes.beats]]
at = 0.58
action = "overload"
target = "latency-meter"
description = "扫描线变慢，计算次数和延迟仪表进入红色区域"

[[scenes.beats]]
at = 0.80
action = "focus"
target = "candidate-subset"
description = "大部分向量变暗，只保留少量候选点，引出 ANN"

[[scenes]]
id = "s06"
narration_index = 6
title = "HNSW：先走高速，再进小路"
purpose = "concept"
visual_type = "graph-search"
layout = "diagram"
key_points = ["高层稀疏图负责快速跳转", "底层密集图负责精细搜索"]
components = ["hnsw-layers", "graph-nodes", "search-path", "target-node"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "hnsw-layers"
description = "从下到上构建密集层、中间层和稀疏层"

[[scenes.beats]]
at = 0.28
action = "traverse"
target = "search-path"
description = "查询从高层入口进行少量长距离跳转"

[[scenes.beats]]
at = 0.55
action = "descend"
target = "search-path"
description = "路径逐层下沉，候选区域逐渐缩小"

[[scenes.beats]]
at = 0.82
action = "arrive"
target = "target-node"
description = "在底层密集图中找到目标邻居并显示 TopK"

[[scenes]]
id = "s07"
narration_index = 7
title = "IVF：只搜索最可能的城区"
purpose = "concept"
visual_type = "cluster-search"
layout = "diagram"
key_points = ["nlist 决定分多少个簇", "nprobe 决定搜索多少个簇"]
components = ["vector-clusters", "centroids", "query-point", "selected-clusters"]

[[scenes.beats]]
at = 0.00
action = "cluster"
target = "vector-clusters"
description = "散点按颜色聚成多个区域，并出现各簇中心"

[[scenes.beats]]
at = 0.35
action = "enter"
target = "query-point"
description = "查询点进入空间，计算到各个中心的距离"

[[scenes.beats]]
at = 0.62
action = "select"
target = "selected-clusters"
description = "只点亮最近的若干簇，其他区域淡出"

[[scenes.beats]]
at = 0.82
action = "search"
target = "selected-clusters"
description = "在被选中的簇内完成局部扫描并返回 TopK"

[[scenes]]
id = "s08"
narration_index = 8
title = "PQ：用短编码代替长向量"
purpose = "concept"
visual_type = "compression"
layout = "diagram"
key_points = ["长向量切成多个子向量", "每段映射为短编码", "内存下降，精度有损"]
components = ["long-vector", "vector-segments", "codebooks", "memory-bars"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "long-vector"
description = "显示一条由大量浮点数组成的长向量"

[[scenes.beats]]
at = 0.28
action = "slice"
target = "vector-segments"
description = "长向量按颜色切成多个子向量"

[[scenes.beats]]
at = 0.52
action = "encode"
target = "codebooks"
description = "每个子向量连接到码本并替换为短编码"

[[scenes.beats]]
at = 0.76
action = "compare"
target = "memory-bars"
description = "原始内存条明显缩短，同时出现轻微精度损失提示"

[[scenes]]
id = "s09"
narration_index = 9
title = "工程上没有免费的午餐"
purpose = "comparison"
visual_type = "dashboard"
layout = "dashboard"
key_points = ["Recall：找全了吗", "QPS：每秒处理多少", "Latency：一次要等多久", "Memory：要花多少资源"]
components = ["recall-gauge", "qps-counter", "latency-chart", "memory-meter", "tradeoff-radar"]

[[scenes.beats]]
at = 0.00
action = "reveal"
target = "recall-gauge"
description = "显示 Recall 仪表并标出该找到的结果"

[[scenes.beats]]
at = 0.22
action = "reveal"
target = "qps-counter"
description = "加入 QPS 计数器并展示吞吐变化"

[[scenes.beats]]
at = 0.44
action = "reveal"
target = "latency-chart"
description = "加入 P50、P95、P99 延迟曲线"

[[scenes.beats]]
at = 0.66
action = "reveal"
target = "memory-meter"
description = "加入内存成本条形图"

[[scenes.beats]]
at = 0.82
action = "balance"
target = "tradeoff-radar"
description = "拖动索引参数时四项指标互相变化，体现工程权衡"

[[scenes]]
id = "s10"
narration_index = 10
title = "向量检索的组合拳"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["表示学习", "距离计算", "索引加速", "下一章：Milvus 如何工程化落地"]
components = ["three-stage-map", "chapter-progress", "next-chapter-card"]

[[scenes.beats]]
at = 0.00
action = "assemble"
target = "three-stage-map"
description = "Embedding、Metric、ANN 三个模块依次组合成完整检索链路"

[[scenes.beats]]
at = 0.38
action = "recap"
target = "chapter-progress"
description = "回放 HNSW、IVF、PQ 和四项指标的缩略图"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "检索链路折叠成 Milvus 系统图标，预告下一章整体架构"
```

## 人工检查

- [x] 10 个 Scene 与当前 10 段旁白、10 条 timing 数据一致
- [x] Scene 内使用相对 Beat，不手写绝对秒数
- [x] HNSW、IVF、PQ 和距离度量都有过程型动态图解
- [x] 屏幕信息是知识摘要，不复制整段旁白
- [x] 使用 HyperFrames + SVG/CSS/GSAP/Canvas，不接入 Motion Canvas
- [ ] 第一章新 HTML 完成后检查字幕安全区、中文字体和 1920×1080 构图
- [ ] 渲染后抽查每个 Scene 的开头、中点、结尾
