# Chapter 23 RAG 知识库实战视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/23-RAG知识库实战.md`
- 核心问题：用可视化方式讲清《23 RAG 知识库实战》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "23"
title = "RAG 知识库实战"
source_doc = "../../milvus-master-course/docs/23-RAG知识库实战.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "从文档解析、切分、入库，到检索、生成、API接口，全流…"
purpose = "hook"
visual_type = "learning-map"
layout = "full"
key_points = ["上一章我们理解了RAG的架构，这一章动手搭建一个完整的RAG知识库系统", "从文档解析、切分、入库，到检索、生成、API接口，全流程跑通", "用的是项目里的demos/rag-system，基于FastAPI加Milvus加…"]
components = ["chapter-map", "learning-goals", "progress-path"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "chapter-map"
description = "建立场景主题：上一章我们理解了RAG的架构，这一章动手搭建一个完整的RAG知识库系统"

[[scenes.beats]]
at = 0.36
action = "connect"
target = "learning-goals"
description = "用动态图解展开：从文档解析、切分、入库，到检索、生成、API接口，全流程跑通"

[[scenes.beats]]
at = 0.72
action = "preview"
target = "progress-path"
description = "突出结论并承接下一段：用的是项目里的demos/rag-system，基于FastAPI加Milvus加…"

[[scenes]]
id = "s02"
narration_index = 2
title = "先看整体架构"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["先看整体架构", "四个模块：config.py管配置，embeddings.py管向量编码，vect…", "数据流是：文档上传、切分、编码、入库"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：先看整体架构"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：四个模块：config.py管配置，embeddings.py管向量编码，vect…"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：数据流是：文档上传、切分、编码、入库"

[[scenes]]
id = "s03"
narration_index = 3
title = "文档入库流程"
purpose = "concept"
visual_type = "code-terminal"
layout = "code"
key_points = ["文档入库流程", "第一步解析：支持纯文本、Markdown、PDF", "第二步切分：按段落切，每段200到500字，重叠50字"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：文档入库流程"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：第一步解析：支持纯文本、Markdown、PDF"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：第二步切分：按段落切，每段200到500字，重叠50字"

[[scenes]]
id = "s04"
narration_index = 4
title = "检索流程"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["检索流程", "用户提问进来，先用同一个Embedding模型编码成向量", "然后调Milvus的search，TopK设5到10"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：检索流程"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：用户提问进来，先用同一个Embedding模型编码成向量"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：然后调Milvus的search，TopK设5到10"

[[scenes]]
id = "s05"
narration_index = 5
title = "生成流程"
purpose = "concept"
visual_type = "code-terminal"
layout = "code"
key_points = ["生成流程", "把检索到的Chunk按相关度排序，拼成上下文", "Prompt模板是：系统提示加上下文加用户问题"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：生成流程"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：把检索到的Chunk按相关度排序，拼成上下文"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：Prompt模板是：系统提示加上下文加用户问题"

[[scenes]]
id = "s06"
narration_index = 6
title = "几个工程细节"
purpose = "concept"
visual_type = "code-terminal"
layout = "code"
key_points = ["几个工程细节", "Embedding模型在启动时加载一次，后续复用，避免每次请求都加载", "Collection如果不存在就自动创建，存在就直接用"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：几个工程细节"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：Embedding模型在启动时加载一次，后续复用，避免每次请求都加载"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：Collection如果不存在就自动创建，存在就直接用"

[[scenes]]
id = "s07"
narration_index = 7
title = "这个系统的局限性"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["这个系统的局限性", "切分策略比较简单，复杂文档可能切得不好", "没有Query Rewrite，用户问题表述不好时检索效果差"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：这个系统的局限性"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：切分策略比较简单，复杂文档可能切得不好"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：没有Query Rewrite，用户问题表述不好时检索效果差"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "一个最小可用的RAG系统就是：切分加编码加入库加检索加生成", "五个步骤，几百行代码"]
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
description = "用动态图解展开：一个最小可用的RAG系统就是：切分加编码加入库加检索加生成"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：五个步骤，几百行代码"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
