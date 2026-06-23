# Chapter 10 IVF 原理与实战视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/10-IVF原理与实战.md`
- 核心问题：用可视化方式讲清《10 IVF 原理与实战》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "10"
title = "IVF 原理与实战"
source_doc = "../../milvus-master-course/docs/10-IVF原理与实战.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "IVF是最经典的向量索引之一，理解它的原理和调参方法…"
purpose = "hook"
visual_type = "learning-map"
layout = "full"
key_points = ["上一章我们总览了五种索引，这一章深入IVF", "IVF是最经典的向量索引之一，理解它的原理和调参方法，对后面学HNSW和PQ都有帮助", "我们搞清楚三件事：IVF怎么建、怎么搜、nlist和nprobe怎么调"]
components = ["chapter-map", "learning-goals", "progress-path"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "chapter-map"
description = "建立场景主题：上一章我们总览了五种索引，这一章深入IVF"

[[scenes.beats]]
at = 0.36
action = "connect"
target = "learning-goals"
description = "用动态图解展开：IVF是最经典的向量索引之一，理解它的原理和调参方法，对后面学HNSW和PQ都有帮助"

[[scenes.beats]]
at = 0.72
action = "preview"
target = "progress-path"
description = "突出结论并承接下一段：我们搞清楚三件事：IVF怎么建、怎么搜、nlist和nprobe怎么调"

[[scenes]]
id = "s02"
narration_index = 2
title = "IVF的构建过程分两步"
purpose = "concept"
visual_type = "cluster-search"
layout = "diagram"
key_points = ["IVF的构建过程分两步", "第一步，用KMeans对所有向量做聚类，生成nlist个聚类中心", "第二步，把每条向量分配到离它最近的中心，形成nlist个倒排列表"]
components = ["clusters", "centroids", "query-node", "selected-regions"]

[[scenes.beats]]
at = 0.00
action = "cluster"
target = "clusters"
description = "建立场景主题：IVF的构建过程分两步"

[[scenes.beats]]
at = 0.36
action = "probe"
target = "centroids"
description = "用动态图解展开：第一步，用KMeans对所有向量做聚类，生成nlist个聚类中心"

[[scenes.beats]]
at = 0.72
action = "select"
target = "query-node"
description = "突出结论并承接下一段：第二步，把每条向量分配到离它最近的中心，形成nlist个倒排列表"

[[scenes]]
id = "s03"
narration_index = 3
title = "搜索时也是两步"
purpose = "concept"
visual_type = "cluster-search"
layout = "diagram"
key_points = ["搜索时也是两步", "第一步，计算查询向量和所有nlist个中心的距离，找出最近的nprobe个中心", "第二步，扫描这nprobe个列表里的所有向量，逐一计算距离，取TopK"]
components = ["clusters", "centroids", "query-node", "selected-regions"]

[[scenes.beats]]
at = 0.00
action = "cluster"
target = "clusters"
description = "建立场景主题：搜索时也是两步"

[[scenes.beats]]
at = 0.36
action = "probe"
target = "centroids"
description = "用动态图解展开：第一步，计算查询向量和所有nlist个中心的距离，找出最近的nprobe个中心"

[[scenes.beats]]
at = 0.72
action = "select"
target = "query-node"
description = "突出结论并承接下一段：第二步，扫描这nprobe个列表里的所有向量，逐一计算距离，取TopK"

[[scenes]]
id = "s04"
narration_index = 4
title = "nlist怎么设"
purpose = "concept"
visual_type = "cluster-search"
layout = "diagram"
key_points = ["nlist怎么设", "经验公式是4乘以根号N", "十万数据设128到256，一百万设1024到4096，一千万设4096到16384"]
components = ["clusters", "centroids", "query-node", "selected-regions"]

[[scenes.beats]]
at = 0.00
action = "cluster"
target = "clusters"
description = "建立场景主题：nlist怎么设"

[[scenes.beats]]
at = 0.36
action = "probe"
target = "centroids"
description = "用动态图解展开：经验公式是4乘以根号N"

[[scenes.beats]]
at = 0.72
action = "select"
target = "query-node"
description = "突出结论并承接下一段：十万数据设128到256，一百万设1024到4096，一千万设4096到16384"

[[scenes]]
id = "s05"
narration_index = 5
title = "nprobe怎么调"
purpose = "concept"
visual_type = "cluster-search"
layout = "diagram"
key_points = ["nprobe怎么调", "nprobe决定了搜索时访问多少个列表", "较小的nprobe通常更快但更容易漏召回"]
components = ["clusters", "centroids", "query-node", "selected-regions"]

[[scenes.beats]]
at = 0.00
action = "cluster"
target = "clusters"
description = "建立场景主题：nprobe怎么调"

[[scenes.beats]]
at = 0.36
action = "probe"
target = "centroids"
description = "用动态图解展开：nprobe决定了搜索时访问多少个列表"

[[scenes.beats]]
at = 0.72
action = "select"
target = "query-node"
description = "突出结论并承接下一段：较小的nprobe通常更快但更容易漏召回"

[[scenes]]
id = "s06"
narration_index = 6
title = "IVF有三个变体"
purpose = "concept"
visual_type = "compression"
layout = "diagram"
key_points = ["IVF有三个变体", "IVF_FLAT：列表里存原始向量，精度最高，内存最大", "IVF_SQ8：列表里存量化后的向量，每个float32压成int8，内存省四分之…"]
components = ["source-vector", "segments", "codebook", "memory-bars"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "source-vector"
description = "建立场景主题：IVF有三个变体"

[[scenes.beats]]
at = 0.36
action = "encode"
target = "segments"
description = "用动态图解展开：IVF_FLAT：列表里存原始向量，精度最高，内存最大"

[[scenes.beats]]
at = 0.72
action = "compare"
target = "codebook"
description = "突出结论并承接下一段：IVF_SQ8：列表里存量化后的向量，每个float32压成int8，内存省四分之…"

[[scenes]]
id = "s07"
narration_index = 7
title = "在Milvus里用IVF很简单"
purpose = "concept"
visual_type = "cluster-search"
layout = "diagram"
key_points = ["在Milvus里用IVF很简单", "创建索引时指定index_type为IVF_FLAT，params里设nlist", "搜索时在search_params里设nprobe"]
components = ["clusters", "centroids", "query-node", "selected-regions"]

[[scenes.beats]]
at = 0.00
action = "cluster"
target = "clusters"
description = "建立场景主题：在Milvus里用IVF很简单"

[[scenes.beats]]
at = 0.36
action = "probe"
target = "centroids"
description = "用动态图解展开：创建索引时指定index_type为IVF_FLAT，params里设nlist"

[[scenes.beats]]
at = 0.72
action = "select"
target = "query-node"
description = "突出结论并承接下一段：搜索时在search_params里设nprobe"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "IVF的核心是分区搜索：nlist决定分多少区，nprobe决定搜多少区", "调参的本质是在召回率和延迟之间找平衡"]
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
description = "用动态图解展开：IVF的核心是分区搜索：nlist决定分多少区，nprobe决定搜多少区"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：调参的本质是在召回率和延迟之间找平衡"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
