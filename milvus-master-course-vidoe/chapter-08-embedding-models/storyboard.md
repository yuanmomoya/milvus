# Chapter 08 Embedding 模型详解视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/08-Embedding模型详解.md`
- 核心问题：用可视化方式讲清《08 Embedding 模型详解》中的关键概念、工程流程与选择依据
- 场景数量：7 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "08"
title = "Embedding 模型详解"
source_doc = "../../milvus-master-course/docs/08-Embedding模型详解.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "Embedding模型会显著影响检索质量，但切分、数据…"
purpose = "hook"
visual_type = "learning-map"
layout = "full"
key_points = ["上一章我们聊了数据建模，知道了向量从哪来", "Embedding模型会显著影响检索质量，但切分、数据质量和评测方法同样重要", "这一章深入模型选型：中文模型怎么评估、API模型和本地模型怎么选、批量编码怎么做…"]
components = ["chapter-map", "learning-goals", "progress-path"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "chapter-map"
description = "建立场景主题：上一章我们聊了数据建模，知道了向量从哪来"

[[scenes.beats]]
at = 0.36
action = "connect"
target = "learning-goals"
description = "用动态图解展开：Embedding模型会显著影响检索质量，但切分、数据质量和评测方法同样重要"

[[scenes.beats]]
at = 0.72
action = "preview"
target = "progress-path"
description = "突出结论并承接下一段：这一章深入模型选型：中文模型怎么评估、API模型和本地模型怎么选、批量编码怎么做…"

[[scenes]]
id = "s02"
narration_index = 2
title = "先建立一个认知：Embedding模型决定搜索质量的上限"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["先建立一个认知：Embedding模型决定搜索质量的上限", "索引参数、搜索策略只能在这个上限内优化", "选错模型，后面怎么调都白搭"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：先建立一个认知：Embedding模型决定搜索质量的上限"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：索引参数、搜索策略只能在这个上限内优化"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：选错模型，后面怎么调都白搭"

[[scenes]]
id = "s03"
narration_index = 3
title = "中文文本场景，推荐BGE系列"
purpose = "concept"
visual_type = "vector-space"
layout = "diagram"
key_points = ["中文文本场景，推荐BGE系列", "bge-small-zh，512维，90兆，速度快，适合资源受限或快速原型", "bge-base-zh，768维，400兆，质量和速度平衡好，通用首选"]
components = ["vector-points", "query-node", "distance-lines", "topk-ring"]

[[scenes.beats]]
at = 0.00
action = "scatter"
target = "vector-points"
description = "建立场景主题：中文文本场景，推荐BGE系列"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "query-node"
description = "用动态图解展开：bge-small-zh，512维，90兆，速度快，适合资源受限或快速原型"

[[scenes.beats]]
at = 0.72
action = "select"
target = "distance-lines"
description = "突出结论并承接下一段：bge-base-zh，768维，400兆，质量和速度平衡好，通用首选"

[[scenes]]
id = "s04"
narration_index = 4
title = "本地部署用sentence-transformers库…"
purpose = "demo"
visual_type = "code-terminal"
layout = "code"
key_points = ["本地部署用sentence-transformers库，三行代码加载模型", "model等于SentenceTransformer加模型名，然后model.en…", "第一次加载会下载模型文件，后续直接从缓存读"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：本地部署用sentence-transformers库，三行代码加载模型"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：model等于SentenceTransformer加模型名，然后model.en…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：第一次加载会下载模型文件，后续直接从缓存读"

[[scenes]]
id = "s05"
narration_index = 5
title = "批量编码是生产环境的关键"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["批量编码是生产环境的关键", "不要一条一条编码，要批量", "sentence-transformers的encode方法天然支持传入列表"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：批量编码是生产环境的关键"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：不要一条一条编码，要批量"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：sentence-transformers的encode方法天然支持传入列表"

[[scenes]]
id = "s06"
narration_index = 6
title = "说模型升级"
purpose = "concept"
visual_type = "code-terminal"
layout = "code"
key_points = ["最后说模型升级", "总有一天你会换更好的模型", "换模型意味着所有向量都要重新编码"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：最后说模型升级"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：总有一天你会换更好的模型"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：换模型意味着所有向量都要重新编码"

[[scenes]]
id = "s07"
narration_index = 7
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "Embedding模型选型看质量、速度、成本、许可证和部署约束", "bge系列可以作为中文场景的候选，API模型可以减少部署工作，但最终必须用自己的标…"]
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
description = "用动态图解展开：Embedding模型选型看质量、速度、成本、许可证和部署约束"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：bge系列可以作为中文场景的候选，API模型可以减少部署工作，但最终必须用自己的标…"
```

## 人工检查

- [x] 7 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
