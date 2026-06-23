# Chapter 31 CLIP 多模态检索视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/31-CLIP多模态检索.md`
- 核心问题：用可视化方式讲清《31 CLIP 多模态检索》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "31"
title = "CLIP 多模态检索"
source_doc = "../../milvus-master-course/docs/31-CLIP多模态检索.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "CLIP不只是以图搜图，它能实现文本、图片、甚至视频帧…"
purpose = "hook"
visual_type = "learning-map"
layout = "full"
key_points = ["上一章我们用CLIP做了图片检索，这一章深入CLIP的多模态能力", "CLIP不只是以图搜图，它能实现文本、图片、甚至视频帧之间的跨模态检索", "我们看几个高级玩法：多模态融合搜索、零样本分类、以及多模态RAG"]
components = ["chapter-map", "learning-goals", "progress-path"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "chapter-map"
description = "建立场景主题：上一章我们用CLIP做了图片检索，这一章深入CLIP的多模态能力"

[[scenes.beats]]
at = 0.36
action = "connect"
target = "learning-goals"
description = "用动态图解展开：CLIP不只是以图搜图，它能实现文本、图片、甚至视频帧之间的跨模态检索"

[[scenes.beats]]
at = 0.72
action = "preview"
target = "progress-path"
description = "突出结论并承接下一段：我们看几个高级玩法：多模态融合搜索、零样本分类、以及多模态RAG"

[[scenes]]
id = "s02"
narration_index = 2
title = "先回顾CLIP的原理"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["先回顾CLIP的原理", "CLIP有两个编码器：文本编码器和图片编码器", "训练时用海量的图文对，让配对的图文向量靠近，不配对的远离"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：先回顾CLIP的原理"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：CLIP有两个编码器：文本编码器和图片编码器"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：训练时用海量的图文对，让配对的图文向量靠近，不配对的远离"

[[scenes]]
id = "s03"
narration_index = 3
title = "第一个高级玩法：多模态融合搜索"
purpose = "concept"
visual_type = "vector-space"
layout = "diagram"
key_points = ["第一个高级玩法：多模态融合搜索", "用户同时提供一张图片和一段文字描述，比如上传一件红色连衣裙的图片，加文字\"类似款式…", "把图片向量和文字向量加权平均，得到融合向量，用这个向量搜索"]
components = ["vector-points", "query-node", "distance-lines", "topk-ring"]

[[scenes.beats]]
at = 0.00
action = "scatter"
target = "vector-points"
description = "建立场景主题：第一个高级玩法：多模态融合搜索"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "query-node"
description = "用动态图解展开：用户同时提供一张图片和一段文字描述，比如上传一件红色连衣裙的图片，加文字\"类似款式…"

[[scenes.beats]]
at = 0.72
action = "select"
target = "distance-lines"
description = "突出结论并承接下一段：把图片向量和文字向量加权平均，得到融合向量，用这个向量搜索"

[[scenes]]
id = "s04"
narration_index = 4
title = "第二个玩法：零样本分类"
purpose = "concept"
visual_type = "vector-space"
layout = "diagram"
key_points = ["第二个玩法：零样本分类", "不需要训练分类器，直接用CLIP判断图片属于哪个类别", "把所有类别名编码成文本向量，把待分类图片编码成图片向量，看图片向量和哪个类别向量最近"]
components = ["vector-points", "query-node", "distance-lines", "topk-ring"]

[[scenes.beats]]
at = 0.00
action = "scatter"
target = "vector-points"
description = "建立场景主题：第二个玩法：零样本分类"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "query-node"
description = "用动态图解展开：不需要训练分类器，直接用CLIP判断图片属于哪个类别"

[[scenes.beats]]
at = 0.72
action = "select"
target = "distance-lines"
description = "突出结论并承接下一段：把所有类别名编码成文本向量，把待分类图片编码成图片向量，看图片向量和哪个类别向量最近"

[[scenes]]
id = "s05"
narration_index = 5
title = "第三个玩法：多模态RAG"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["第三个玩法：多模态RAG", "知识库里不只有文本，还有图表、截图、架构图", "用CLIP把图片也编码入库"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：第三个玩法：多模态RAG"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：知识库里不只有文本，还有图表、截图、架构图"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：用CLIP把图片也编码入库"

[[scenes]]
id = "s06"
narration_index = 6
title = "工程实现上，多模态Collection的Schema需…"
purpose = "demo"
visual_type = "code-terminal"
layout = "code"
key_points = ["工程实现上，多模态Collection的Schema需要一个modality字段标…", "搜索时可以按模态过滤：只搜图片、只搜文本、或者混合搜索", "向量字段只有一个，因为CLIP把所有模态映射到同一个空间"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：工程实现上，多模态Collection的Schema需要一个modality字段标…"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：搜索时可以按模态过滤：只搜图片、只搜文本、或者混合搜索"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：向量字段只有一个，因为CLIP把所有模态映射到同一个空间"

[[scenes]]
id = "s07"
narration_index = 7
title = "CLIP的局限性"
purpose = "concept"
visual_type = "vector-space"
layout = "diagram"
key_points = ["CLIP的局限性", "第一，中文理解不如专门的中文模型", "解决方案是用Chinese-CLIP或者多语言CLIP"]
components = ["vector-points", "query-node", "distance-lines", "topk-ring"]

[[scenes.beats]]
at = 0.00
action = "scatter"
target = "vector-points"
description = "建立场景主题：CLIP的局限性"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "query-node"
description = "用动态图解展开：第一，中文理解不如专门的中文模型"

[[scenes.beats]]
at = 0.72
action = "select"
target = "distance-lines"
description = "突出结论并承接下一段：解决方案是用Chinese-CLIP或者多语言CLIP"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "CLIP是多模态检索的瑞士军刀：跨模态搜索、融合搜索、零样本分类、多模态RAG都能做", "核心是一个统一的向量空间"]
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
description = "用动态图解展开：CLIP是多模态检索的瑞士军刀：跨模态搜索、融合搜索、零样本分类、多模态RAG都能做"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：核心是一个统一的向量空间"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
