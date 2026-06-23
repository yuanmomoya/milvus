# Chapter 12 PQ 与量化压缩视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/12-PQ与量化压缩.md`
- 核心问题：用可视化方式讲清《12 PQ 与量化压缩》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "12"
title = "PQ 与量化压缩"
source_doc = "../../milvus-master-course/docs/12-PQ与量化压缩.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "一亿条768维向量，光原始数据就要300G内存"
purpose = "hook"
visual_type = "hook-comparison"
layout = "split"
key_points = ["上一章HNSW很好用，但有个问题：内存太贵", "一亿条768维向量，光原始数据就要300G内存", "这一章我们学PQ量化压缩：怎么把向量压小几倍到几十倍，用可接受的精度损失换巨大的内…"]
components = ["question-card", "before-after-panels", "conflict-highlight"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "question-card"
description = "建立场景主题：上一章HNSW很好用，但有个问题：内存太贵"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "before-after-panels"
description = "用动态图解展开：一亿条768维向量，光原始数据就要300G内存"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "conflict-highlight"
description = "突出结论并承接下一段：这一章我们学PQ量化压缩：怎么把向量压小几倍到几十倍，用可接受的精度损失换巨大的内…"

[[scenes]]
id = "s02"
narration_index = 2
title = "PQ的全称是Product Quantization…"
purpose = "concept"
visual_type = "compression"
layout = "diagram"
key_points = ["PQ的全称是Product Quantization，乘积量化", "核心思想是把一个长向量切成若干子段，每段独立做聚类压缩", "比如768维向量切成96段，每段8维"]
components = ["source-vector", "segments", "codebook", "memory-bars"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "source-vector"
description = "建立场景主题：PQ的全称是Product Quantization，乘积量化"

[[scenes.beats]]
at = 0.36
action = "encode"
target = "segments"
description = "用动态图解展开：核心思想是把一个长向量切成若干子段，每段独立做聚类压缩"

[[scenes.beats]]
at = 0.72
action = "compare"
target = "codebook"
description = "突出结论并承接下一段：比如768维向量切成96段，每段8维"

[[scenes]]
id = "s03"
narration_index = 3
title = "具体怎么做"
purpose = "concept"
visual_type = "compression"
layout = "diagram"
key_points = ["具体怎么做", "训练阶段：把所有向量按子段切开，每段独立跑KMeans生成256个中心，形成码本", "编码阶段：每条向量的每个子段，找到最近的中心编号，用这个编号代替原始数据"]
components = ["source-vector", "segments", "codebook", "memory-bars"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "source-vector"
description = "建立场景主题：具体怎么做"

[[scenes.beats]]
at = 0.36
action = "encode"
target = "segments"
description = "用动态图解展开：训练阶段：把所有向量按子段切开，每段独立跑KMeans生成256个中心，形成码本"

[[scenes.beats]]
at = 0.72
action = "compare"
target = "codebook"
description = "突出结论并承接下一段：编码阶段：每条向量的每个子段，找到最近的中心编号，用这个编号代替原始数据"

[[scenes]]
id = "s04"
narration_index = 4
title = "PQ有两个关键参数"
purpose = "concept"
visual_type = "compression"
layout = "diagram"
key_points = ["PQ有两个关键参数", "m是子段数，编码大小大约是m乘以nbits再除以8", "nbits等于8时，每段占1字节，所以m越大，编码越长、压缩比越低，但通常能保留更…"]
components = ["source-vector", "segments", "codebook", "memory-bars"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "source-vector"
description = "建立场景主题：PQ有两个关键参数"

[[scenes.beats]]
at = 0.36
action = "encode"
target = "segments"
description = "用动态图解展开：m是子段数，编码大小大约是m乘以nbits再除以8"

[[scenes.beats]]
at = 0.72
action = "compare"
target = "codebook"
description = "突出结论并承接下一段：nbits等于8时，每段占1字节，所以m越大，编码越长、压缩比越低，但通常能保留更…"

[[scenes]]
id = "s05"
narration_index = 5
title = "除了PQ还有SQ8，标量量化"
purpose = "concept"
visual_type = "compression"
layout = "diagram"
key_points = ["除了PQ还有SQ8，标量量化", "SQ8更简单：把每个float32直接量化成int8，压缩比固定4倍", "精度损失比PQ小，但压缩比也小"]
components = ["source-vector", "segments", "codebook", "memory-bars"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "source-vector"
description = "建立场景主题：除了PQ还有SQ8，标量量化"

[[scenes.beats]]
at = 0.36
action = "encode"
target = "segments"
description = "用动态图解展开：SQ8更简单：把每个float32直接量化成int8，压缩比固定4倍"

[[scenes.beats]]
at = 0.72
action = "compare"
target = "codebook"
description = "突出结论并承接下一段：精度损失比PQ小，但压缩比也小"

[[scenes]]
id = "s06"
narration_index = 6
title = "在Milvus里怎么用"
purpose = "demo"
visual_type = "graph-search"
layout = "diagram"
key_points = ["在Milvus里怎么用", "IVF_SQ8：IVF加SQ8量化，4倍压缩，精度损失很小", "IVF_PQ：IVF加PQ量化，压缩比可调，精度损失较大但内存省很多"]
components = ["graph-layers", "search-route", "candidate-nodes"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "graph-layers"
description = "建立场景主题：在Milvus里怎么用"

[[scenes.beats]]
at = 0.36
action = "traverse"
target = "search-route"
description = "用动态图解展开：IVF_SQ8：IVF加SQ8量化，4倍压缩，精度损失很小"

[[scenes.beats]]
at = 0.72
action = "arrive"
target = "candidate-nodes"
description = "突出结论并承接下一段：IVF_PQ：IVF加PQ量化，压缩比可调，精度损失较大但内存省很多"

[[scenes]]
id = "s07"
narration_index = 7
title = "量化并不要求所有向量都必须归一化，关键是Embeddi…"
purpose = "concept"
visual_type = "compression"
layout = "diagram"
key_points = ["量化并不要求所有向量都必须归一化，关键是Embedding模型、索引和搜索使用一致…", "COSINE会按余弦公式计算，不能把它理解成pymilvus替你改写了原始向量", "如果想让IP近似余弦排序，需要在写入和查询两侧显式做一致的归一化"]
components = ["source-vector", "segments", "codebook", "memory-bars"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "source-vector"
description = "建立场景主题：量化并不要求所有向量都必须归一化，关键是Embedding模型、索引和搜索使用一致…"

[[scenes.beats]]
at = 0.36
action = "encode"
target = "segments"
description = "用动态图解展开：COSINE会按余弦公式计算，不能把它理解成pymilvus替你改写了原始向量"

[[scenes.beats]]
at = 0.72
action = "compare"
target = "codebook"
description = "突出结论并承接下一段：如果想让IP近似余弦排序，需要在写入和查询两侧显式做一致的归一化"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "PQ是用精度换内存的利器", "按编码本身估算，32倍压缩可以把约300G的原始向量压到约10G，但实际部署还要加…"]
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
description = "用动态图解展开：PQ是用精度换内存的利器"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：按编码本身估算，32倍压缩可以把约300G的原始向量压到约10G，但实际部署还要加…"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
