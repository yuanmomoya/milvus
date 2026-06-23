# Chapter 00 教程规划与学习路径视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/00-教程规划与学习路径.md`
- 核心问题：用可视化方式讲清《00 教程规划与学习路径》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "00"
title = "教程规划与学习路径"
source_doc = "../../milvus-master-course/docs/00-教程规划与学习路径.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "欢迎来到Milvus从入门到精通"
purpose = "hook"
visual_type = "learning-map"
layout = "full"
key_points = ["欢迎来到Milvus从入门到精通", "在正式开始之前，这一章我们先把全貌摆出来：这套教程要带你到哪里、四十个章节怎么编排…", "看完这一章，你心里会有一张清晰的学习地图"]
components = ["chapter-map", "learning-goals", "progress-path"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "chapter-map"
description = "建立场景主题：欢迎来到Milvus从入门到精通"

[[scenes.beats]]
at = 0.36
action = "connect"
target = "learning-goals"
description = "用动态图解展开：在正式开始之前，这一章我们先把全貌摆出来：这套教程要带你到哪里、四十个章节怎么编排…"

[[scenes.beats]]
at = 0.72
action = "preview"
target = "progress-path"
description = "突出结论并承接下一段：看完这一章，你心里会有一张清晰的学习地图"

[[scenes]]
id = "s02"
narration_index = 2
title = "目标"
purpose = "diagnosis"
visual_type = "error-diagnosis"
layout = "diagram"
key_points = ["目标", "学完这套教程，你能从三个层面掌握Milvus", "原理层面：解释清楚ANN、HNSW、IVF、PQ这些算法是怎么工作的"]
components = ["symptom-card", "diagnosis-tree", "fix-checklist"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "symptom-card"
description = "建立场景主题：目标"

[[scenes.beats]]
at = 0.36
action = "trace"
target = "diagnosis-tree"
description = "用动态图解展开：学完这套教程，你能从三个层面掌握Milvus"

[[scenes.beats]]
at = 0.72
action = "resolve"
target = "fix-checklist"
description = "突出结论并承接下一段：原理层面：解释清楚ANN、HNSW、IVF、PQ这些算法是怎么工作的"

[[scenes]]
id = "s03"
narration_index = 3
title = "整个教程分四个阶段，对应仓库的四个目录"
purpose = "concept"
visual_type = "dashboard"
layout = "dashboard"
key_points = ["整个教程分四个阶段，对应仓库的四个目录", "第一阶段是学习地图和项目骨架，README给出全局规划", "第二阶段是docs目录下的四十章Markdown教程，逐章深入"]
components = ["metric-cards", "trend-chart", "threshold-line", "tradeoff-control"]

[[scenes.beats]]
at = 0.00
action = "reveal"
target = "metric-cards"
description = "建立场景主题：整个教程分四个阶段，对应仓库的四个目录"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "trend-chart"
description = "用动态图解展开：第一阶段是学习地图和项目骨架，README给出全局规划"

[[scenes.beats]]
at = 0.72
action = "balance"
target = "threshold-line"
description = "突出结论并承接下一段：第二阶段是docs目录下的四十章Markdown教程，逐章深入"

[[scenes]]
id = "s04"
narration_index = 4
title = "四十章按七个主题分组"
purpose = "concept"
visual_type = "graph-search"
layout = "diagram"
key_points = ["四十章按七个主题分组", "第1章到第5章是基础：解释向量检索、启动Milvus、完成基本的增删改查和搜索", "第6章到第9章是建模：设计Collection、字段、Embedding和索引"]
components = ["graph-layers", "search-route", "candidate-nodes"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "graph-layers"
description = "建立场景主题：四十章按七个主题分组"

[[scenes.beats]]
at = 0.36
action = "traverse"
target = "search-route"
description = "用动态图解展开：第1章到第5章是基础：解释向量检索、启动Milvus、完成基本的增删改查和搜索"

[[scenes.beats]]
at = 0.72
action = "arrive"
target = "candidate-nodes"
description = "突出结论并承接下一段：第6章到第9章是建模：设计Collection、字段、Embedding和索引"

[[scenes]]
id = "s05"
narration_index = 5
title = "继续往后"
purpose = "diagnosis"
visual_type = "error-diagnosis"
layout = "diagram"
key_points = ["继续往后", "第18章到第21章是生产章节：规划集群、高可用、监控、备份和容量", "第22章到第29章是RAG专题：知识库问答、召回优化、Rerank重排、多路召回"]
components = ["symptom-card", "diagnosis-tree", "fix-checklist"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "symptom-card"
description = "建立场景主题：继续往后"

[[scenes.beats]]
at = 0.36
action = "trace"
target = "diagnosis-tree"
description = "用动态图解展开：第18章到第21章是生产章节：规划集群、高可用、监控、备份和容量"

[[scenes.beats]]
at = 0.72
action = "resolve"
target = "fix-checklist"
description = "突出结论并承接下一段：第22章到第29章是RAG专题：知识库问答、召回优化、Rerank重排、多路召回"

[[scenes]]
id = "s06"
narration_index = 6
title = "每一章都用统一结构"
purpose = "demo"
visual_type = "architecture"
layout = "diagram"
key_points = ["每一章都用统一结构", "学习目标、核心概念、原理讲解、Mermaid图解、完整代码入口、Demo、常见错误…", "重点章节会额外给出参数表、生产经验和架构权衡"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：每一章都用统一结构"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：学习目标、核心概念、原理讲解、Mermaid图解、完整代码入口、Demo、常见错误…"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：重点章节会额外给出参数表、生产经验和架构权衡"

[[scenes]]
id = "s07"
narration_index = 7
title = "说推荐节奏"
purpose = "demo"
visual_type = "code-terminal"
layout = "code"
key_points = ["最后说推荐节奏", "第一步，先跑通docker compose up命令，把demos里的basic-…", "第二步，每读完一个索引章节，就用demos的benchmark改参数验证"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：最后说推荐节奏"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：第一步，先跑通docker compose up命令，把demos里的basic-…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：第二步，每读完一个索引章节，就用demos的benchmark改参数验证"

[[scenes]]
id = "s08"
narration_index = 8
title = "这就是全貌"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，这就是全貌", "理论加实战、原理加生产，四十章一步一步把你从向量数据库新手带到能独立设计企业级检索…", "下一章我们正式开始，从向量数据库的基本概念讲起"]
components = ["knowledge-map", "chapter-progress", "next-chapter-card"]

[[scenes.beats]]
at = 0.00
action = "assemble"
target = "knowledge-map"
description = "建立场景主题：好，这就是全貌"

[[scenes.beats]]
at = 0.36
action = "recap"
target = "chapter-progress"
description = "用动态图解展开：理论加实战、原理加生产，四十章一步一步把你从向量数据库新手带到能独立设计企业级检索…"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：下一章我们正式开始，从向量数据库的基本概念讲起"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
