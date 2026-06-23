# Chapter 32 视频检索思路视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/32-视频检索思路.md`
- 核心问题：用可视化方式讲清《32 视频检索思路》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "32"
title = "视频检索思路"
source_doc = "../../milvus-master-course/docs/32-视频检索思路.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "视频本质上是一系列图片帧加上音频"
purpose = "hook"
visual_type = "learning-map"
layout = "full"
key_points = ["上一章我们做了图片检索，视频检索是它的自然延伸", "视频本质上是一系列图片帧加上音频", "这一章我们聊视频检索的思路：怎么把视频变成可搜索的向量、怎么定位到具体片段、以及工…"]
components = ["chapter-map", "learning-goals", "progress-path"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "chapter-map"
description = "建立场景主题：上一章我们做了图片检索，视频检索是它的自然延伸"

[[scenes.beats]]
at = 0.36
action = "connect"
target = "learning-goals"
description = "用动态图解展开：视频本质上是一系列图片帧加上音频"

[[scenes.beats]]
at = 0.72
action = "preview"
target = "progress-path"
description = "突出结论并承接下一段：这一章我们聊视频检索的思路：怎么把视频变成可搜索的向量、怎么定位到具体片段、以及工…"

[[scenes]]
id = "s02"
narration_index = 2
title = "视频检索的核心思路是：把视频拆成帧或片段，每个片段提取…"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["视频检索的核心思路是：把视频拆成帧或片段，每个片段提取特征向量存入Milvus", "搜索时用文字描述或图片作为查询，找到最相似的视频片段，返回对应的时间戳", "用户就能直接跳转到视频的相关位置"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：视频检索的核心思路是：把视频拆成帧或片段，每个片段提取特征向量存入Milvus"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：搜索时用文字描述或图片作为查询，找到最相似的视频片段，返回对应的时间戳"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：用户就能直接跳转到视频的相关位置"

[[scenes]]
id = "s03"
narration_index = 3
title = "帧采样策略"
purpose = "concept"
visual_type = "metric-comparison"
layout = "split"
key_points = ["帧采样策略", "不可能每一帧都编码，一分钟视频有1800帧，太多了", "常见做法是每秒采1到2帧，或者用关键帧检测只取场景变化的帧"]
components = ["comparison-cards", "tradeoff-axis", "decision-marker"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "comparison-cards"
description = "建立场景主题：帧采样策略"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "tradeoff-axis"
description = "用动态图解展开：不可能每一帧都编码，一分钟视频有1800帧，太多了"

[[scenes.beats]]
at = 0.72
action = "decide"
target = "decision-marker"
description = "突出结论并承接下一段：常见做法是每秒采1到2帧，或者用关键帧检测只取场景变化的帧"

[[scenes]]
id = "s04"
narration_index = 4
title = "特征提取有两种方式"
purpose = "concept"
visual_type = "vector-space"
layout = "diagram"
key_points = ["特征提取有两种方式", "第一种：逐帧用CLIP提取图片特征，每帧一个向量", "优点是简单，能做以文搜视频"]
components = ["vector-points", "query-node", "distance-lines", "topk-ring"]

[[scenes.beats]]
at = 0.00
action = "scatter"
target = "vector-points"
description = "建立场景主题：特征提取有两种方式"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "query-node"
description = "用动态图解展开：第一种：逐帧用CLIP提取图片特征，每帧一个向量"

[[scenes.beats]]
at = 0.72
action = "select"
target = "distance-lines"
description = "突出结论并承接下一段：优点是简单，能做以文搜视频"

[[scenes]]
id = "s05"
narration_index = 5
title = "Schema设计"
purpose = "concept"
visual_type = "code-terminal"
layout = "code"
key_points = ["Schema设计", "每条记录对应一个视频片段", "字段包括：video_id、start_time、end_time、frame_u…"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：Schema设计"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：每条记录对应一个视频片段"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：字段包括：video_id、start_time、end_time、frame_u…"

[[scenes]]
id = "s06"
narration_index = 6
title = "工程挑战"
purpose = "concept"
visual_type = "graph-search"
layout = "diagram"
key_points = ["工程挑战", "第一，数据量大", "一个小时的视频按每秒一帧就是3600条记录"]
components = ["graph-layers", "search-route", "candidate-nodes"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "graph-layers"
description = "建立场景主题：工程挑战"

[[scenes.beats]]
at = 0.36
action = "traverse"
target = "search-route"
description = "用动态图解展开：第一，数据量大"

[[scenes.beats]]
at = 0.72
action = "arrive"
target = "candidate-nodes"
description = "突出结论并承接下一段：一个小时的视频按每秒一帧就是3600条记录"

[[scenes]]
id = "s07"
narration_index = 7
title = "一个实用的简化方案：不做逐帧检索，而是对每个视频生成一…"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["一个实用的简化方案：不做逐帧检索，而是对每个视频生成一段文字摘要，用文本向量检索", "用多模态大模型看视频生成描述，然后用文本Embedding入库", "搜索时用文本匹配文本，简单高效"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：一个实用的简化方案：不做逐帧检索，而是对每个视频生成一段文字摘要，用文本向量检索"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：用多模态大模型看视频生成描述，然后用文本Embedding入库"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：搜索时用文本匹配文本，简单高效"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "视频检索的核心是把时间维度的内容离散化成可搜索的片段", "帧采样加CLIP是最通用的方案"]
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
description = "用动态图解展开：视频检索的核心是把时间维度的内容离散化成可搜索的片段"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：帧采样加CLIP是最通用的方案"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
