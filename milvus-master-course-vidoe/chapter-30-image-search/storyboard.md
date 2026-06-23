# Chapter 30 图片检索系统视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/30-图片检索系统.md`
- 核心问题：用可视化方式讲清《30 图片检索系统》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "30"
title = "图片检索系统"
source_doc = "../../milvus-master-course/docs/30-图片检索系统.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "前面二十九章都在聊文本检索，从这一章开始我们进入多模态…"
purpose = "hook"
visual_type = "learning-map"
layout = "full"
key_points = ["前面二十九章都在聊文本检索，从这一章开始我们进入多模态领域", "第一站：图片检索", "用户上传一张图片或输入一段文字描述，系统返回最相似的图片"]
components = ["chapter-map", "learning-goals", "progress-path"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "chapter-map"
description = "建立场景主题：前面二十九章都在聊文本检索，从这一章开始我们进入多模态领域"

[[scenes.beats]]
at = 0.36
action = "connect"
target = "learning-goals"
description = "用动态图解展开：第一站：图片检索"

[[scenes.beats]]
at = 0.72
action = "preview"
target = "progress-path"
description = "突出结论并承接下一段：用户上传一张图片或输入一段文字描述，系统返回最相似的图片"

[[scenes]]
id = "s02"
narration_index = 2
title = "图片检索的核心和文本检索一样：把图片变成向量，存入Mi…"
purpose = "comparison"
visual_type = "pipeline"
layout = "diagram"
key_points = ["图片检索的核心和文本检索一样：把图片变成向量，存入Milvus，搜索时比较向量距离", "区别在于Embedding模型不同", "文本用BGE这类语言模型，图片用视觉模型"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：图片检索的核心和文本检索一样：把图片变成向量，存入Milvus，搜索时比较向量距离"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：区别在于Embedding模型不同"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：文本用BGE这类语言模型，图片用视觉模型"

[[scenes]]
id = "s03"
narration_index = 3
title = "CLIP的特别之处在于：你可以用文字搜图片"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["CLIP的特别之处在于：你可以用文字搜图片", "比如输入\"一只橘猫趴在键盘上\"，CLIP把这段文字编码成向量，和图片向量在同一个空…", "这叫跨模态检索，是CLIP最强大的能力"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：CLIP的特别之处在于：你可以用文字搜图片"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：比如输入\"一只橘猫趴在键盘上\"，CLIP把这段文字编码成向量，和图片向量在同一个空…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：这叫跨模态检索，是CLIP最强大的能力"

[[scenes]]
id = "s04"
narration_index = 4
title = "图片入库流程"
purpose = "concept"
visual_type = "code-terminal"
layout = "code"
key_points = ["图片入库流程", "第一步，收集图片，记录路径或URL", "第二步，用CLIP的图片编码器提取特征向量"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：图片入库流程"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：第一步，收集图片，记录路径或URL"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：第二步，用CLIP的图片编码器提取特征向量"

[[scenes]]
id = "s05"
narration_index = 5
title = "搜索有两种模式"
purpose = "concept"
visual_type = "vector-space"
layout = "diagram"
key_points = ["搜索有两种模式", "以图搜图：用户上传图片，用CLIP图片编码器提取向量，搜索Milvus返回相似图片", "以文搜图：用户输入文字描述，用CLIP文本编码器提取向量，搜索Milvus返回匹配…"]
components = ["vector-points", "query-node", "distance-lines", "topk-ring"]

[[scenes.beats]]
at = 0.00
action = "scatter"
target = "vector-points"
description = "建立场景主题：搜索有两种模式"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "query-node"
description = "用动态图解展开：以图搜图：用户上传图片，用CLIP图片编码器提取向量，搜索Milvus返回相似图片"

[[scenes.beats]]
at = 0.72
action = "select"
target = "distance-lines"
description = "突出结论并承接下一段：以文搜图：用户输入文字描述，用CLIP文本编码器提取向量，搜索Milvus返回匹配…"

[[scenes]]
id = "s06"
narration_index = 6
title = "工程上有几个注意点"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["工程上有几个注意点", "第一，图片预处理：统一resize到模型要求的尺寸，通常224x224", "第二，批量编码：GPU上批量处理图片比逐张快很多"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：工程上有几个注意点"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：第一，图片预处理：统一resize到模型要求的尺寸，通常224x224"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：第二，批量编码：GPU上批量处理图片比逐张快很多"

[[scenes]]
id = "s07"
narration_index = 7
title = "CLIP模型的选择"
purpose = "comparison"
visual_type = "vector-space"
layout = "diagram"
key_points = ["CLIP模型的选择", "clip-vit-base-patch32：512维，速度快，适合入门和资源受限场景", "clip-vit-large-patch14：768维，精度更高，适合对质量要求高…"]
components = ["vector-points", "query-node", "distance-lines", "topk-ring"]

[[scenes.beats]]
at = 0.00
action = "scatter"
target = "vector-points"
description = "建立场景主题：CLIP模型的选择"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "query-node"
description = "用动态图解展开：clip-vit-base-patch32：512维，速度快，适合入门和资源受限场景"

[[scenes.beats]]
at = 0.72
action = "select"
target = "distance-lines"
description = "突出结论并承接下一段：clip-vit-large-patch14：768维，精度更高，适合对质量要求高…"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "图片检索等于CLIP编码加Milvus存储加向量搜索", "支持以图搜图和以文搜图两种模式"]
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
description = "用动态图解展开：图片检索等于CLIP编码加Milvus存储加向量搜索"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：支持以图搜图和以文搜图两种模式"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
