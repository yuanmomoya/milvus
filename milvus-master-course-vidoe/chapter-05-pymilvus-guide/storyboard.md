# Chapter 05 pymilvus 完全指南视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/05-pymilvus完全指南.md`
- 核心问题：用可视化方式讲清《05 pymilvus 完全指南》中的关键概念、工程流程与选择依据
- 场景数量：7 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "05"
title = "pymilvus 完全指南"
source_doc = "../../milvus-master-course/docs/05-pymilvus完全指南.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "搞清楚五件事：怎么连接、怎么定义Schema、怎么建索…"
purpose = "hook"
visual_type = "learning-map"
layout = "full"
key_points = ["上一章我们用Docker把Milvus跑起来了，这一章深入pymilvus这个Py…", "搞清楚五件事：怎么连接、怎么定义Schema、怎么建索引、怎么增删改查、以及生产环…", "这五件事覆盖了日常开发百分之九十的场景"]
components = ["chapter-map", "learning-goals", "progress-path"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "chapter-map"
description = "建立场景主题：上一章我们用Docker把Milvus跑起来了，这一章深入pymilvus这个Py…"

[[scenes.beats]]
at = 0.36
action = "connect"
target = "learning-goals"
description = "用动态图解展开：搞清楚五件事：怎么连接、怎么定义Schema、怎么建索引、怎么增删改查、以及生产环…"

[[scenes.beats]]
at = 0.72
action = "preview"
target = "progress-path"
description = "突出结论并承接下一段：这五件事覆盖了日常开发百分之九十的场景"

[[scenes]]
id = "s02"
narration_index = 2
title = "连接"
purpose = "diagnosis"
visual_type = "error-diagnosis"
layout = "diagram"
key_points = ["连接", "pymilvus提供了MilvusClient这个高层API，三行代码搞定", "传入uri和token就能连上"]
components = ["symptom-card", "diagnosis-tree", "fix-checklist"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "symptom-card"
description = "建立场景主题：连接"

[[scenes.beats]]
at = 0.36
action = "trace"
target = "diagnosis-tree"
description = "用动态图解展开：pymilvus提供了MilvusClient这个高层API，三行代码搞定"

[[scenes.beats]]
at = 0.72
action = "resolve"
target = "fix-checklist"
description = "突出结论并承接下一段：传入uri和token就能连上"

[[scenes]]
id = "s03"
narration_index = 3
title = "连上了，下一步定义Schema"
purpose = "concept"
visual_type = "code-terminal"
layout = "code"
key_points = ["连上了，下一步定义Schema", "Schema就是表结构：主键字段、标量字段、向量字段", "主键推荐用VARCHAR加业务ID，这样才能用upsert做幂等写入"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：连上了，下一步定义Schema"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：Schema就是表结构：主键字段、标量字段、向量字段"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：主键推荐用VARCHAR加业务ID，这样才能用upsert做幂等写入"

[[scenes]]
id = "s04"
narration_index = 4
title = "Schema定义好了，接下来建索引"
purpose = "concept"
visual_type = "graph-search"
layout = "diagram"
key_points = ["Schema定义好了，接下来建索引", "向量索引决定搜索速度和精度", "HNSW适合中小规模、对延迟敏感的场景"]
components = ["graph-layers", "search-route", "candidate-nodes"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "graph-layers"
description = "建立场景主题：Schema定义好了，接下来建索引"

[[scenes.beats]]
at = 0.36
action = "traverse"
target = "search-route"
description = "用动态图解展开：向量索引决定搜索速度和精度"

[[scenes.beats]]
at = 0.72
action = "arrive"
target = "candidate-nodes"
description = "突出结论并承接下一段：HNSW适合中小规模、对延迟敏感的场景"

[[scenes]]
id = "s05"
narration_index = 5
title = "核心来了：增删改查"
purpose = "concept"
visual_type = "code-terminal"
layout = "code"
key_points = ["核心来了：增删改查", "insert写入新数据，upsert写入或覆盖，delete按表达式删除", "search是向量相似度搜索，返回TopK"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：核心来了：增删改查"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：insert写入新数据，upsert写入或覆盖，delete按表达式删除"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：search是向量相似度搜索，返回TopK"

[[scenes]]
id = "s06"
narration_index = 6
title = "说生产级的批量写入"
purpose = "diagnosis"
visual_type = "error-diagnosis"
layout = "diagram"
key_points = ["最后说生产级的批量写入", "一次upsert几万条数据，不要一条一条写", "推荐每批一千到五千条，用循环分批提交"]
components = ["symptom-card", "diagnosis-tree", "fix-checklist"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "symptom-card"
description = "建立场景主题：最后说生产级的批量写入"

[[scenes.beats]]
at = 0.36
action = "trace"
target = "diagnosis-tree"
description = "用动态图解展开：一次upsert几万条数据，不要一条一条写"

[[scenes.beats]]
at = 0.72
action = "resolve"
target = "fix-checklist"
description = "突出结论并承接下一段：推荐每批一千到五千条，用循环分批提交"

[[scenes]]
id = "s07"
narration_index = 7
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "pymilvus的日常就是五个动作：connect、create、insert、s…", "记住用MilvusClient、用upsert、用HNSW加COSINE，这三个默…"]
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
description = "用动态图解展开：pymilvus的日常就是五个动作：connect、create、insert、s…"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：记住用MilvusClient、用upsert、用HNSW加COSINE，这三个默…"
```

## 人工检查

- [x] 7 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
