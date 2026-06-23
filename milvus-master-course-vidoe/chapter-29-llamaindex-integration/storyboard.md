# Chapter 29 LlamaIndex 集成视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/29-LlamaIndex集成.md`
- 核心问题：用可视化方式讲清《29 LlamaIndex 集成》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "29"
title = "LlamaIndex 集成"
source_doc = "../../milvus-master-course/docs/29-LlamaIndex集成.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "LlamaIndex和LangChain的定位不同：L…"
purpose = "hook"
visual_type = "hook-comparison"
layout = "split"
key_points = ["上一章用LangChain集成Milvus，这一章看LlamaIndex", "LlamaIndex和LangChain的定位不同：LangChain是通用的LL…", "如果你的核心需求是把各种数据源高效地接入RAG，LlamaIndex可能更合适"]
components = ["question-card", "before-after-panels", "conflict-highlight"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "question-card"
description = "建立场景主题：上一章用LangChain集成Milvus，这一章看LlamaIndex"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "before-after-panels"
description = "用动态图解展开：LlamaIndex和LangChain的定位不同：LangChain是通用的LL…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "conflict-highlight"
description = "突出结论并承接下一段：如果你的核心需求是把各种数据源高效地接入RAG，LlamaIndex可能更合适"

[[scenes]]
id = "s02"
narration_index = 2
title = "LlamaIndex的核心概念是Index"
purpose = "concept"
visual_type = "metric-comparison"
layout = "split"
key_points = ["LlamaIndex的核心概念是Index", "它把文档加载、切分、编码、存储封装成一个Index对象", "MilvusVectorStore是其中一种存储后端"]
components = ["comparison-cards", "tradeoff-axis", "decision-marker"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "comparison-cards"
description = "建立场景主题：LlamaIndex的核心概念是Index"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "tradeoff-axis"
description = "用动态图解展开：它把文档加载、切分、编码、存储封装成一个Index对象"

[[scenes.beats]]
at = 0.72
action = "decide"
target = "decision-marker"
description = "突出结论并承接下一段：MilvusVectorStore是其中一种存储后端"

[[scenes]]
id = "s03"
narration_index = 3
title = "和LangChain相比，LlamaIndex的优势在…"
purpose = "concept"
visual_type = "code-terminal"
layout = "code"
key_points = ["和LangChain相比，LlamaIndex的优势在数据处理", "它内置了几十种Document Loader：PDF、Word、网页、数据库、API", "切分策略也更丰富：按句子、按段落、按语义边界"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：和LangChain相比，LlamaIndex的优势在数据处理"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：它内置了几十种Document Loader：PDF、Word、网页、数据库、API"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：切分策略也更丰富：按句子、按段落、按语义边界"

[[scenes]]
id = "s04"
narration_index = 4
title = "在LlamaIndex里用Milvus怎么写"
purpose = "demo"
visual_type = "metric-comparison"
layout = "split"
key_points = ["在LlamaIndex里用Milvus怎么写", "三步", "第一步，创建MilvusVectorStore，传入连接参数和Collection名"]
components = ["comparison-cards", "tradeoff-axis", "decision-marker"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "comparison-cards"
description = "建立场景主题：在LlamaIndex里用Milvus怎么写"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "tradeoff-axis"
description = "用动态图解展开：三步"

[[scenes.beats]]
at = 0.72
action = "decide"
target = "decision-marker"
description = "突出结论并承接下一段：第一步，创建MilvusVectorStore，传入连接参数和Collection名"

[[scenes]]
id = "s05"
narration_index = 5
title = "LlamaIndex的高级特性"
purpose = "demo"
visual_type = "pipeline"
layout = "diagram"
key_points = ["LlamaIndex的高级特性", "SubQuestionQueryEngine：把复杂问题拆成多个子问题，分别检索再…", "RouterQueryEngine：根据问题类型路由到不同的检索策略"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：LlamaIndex的高级特性"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：SubQuestionQueryEngine：把复杂问题拆成多个子问题，分别检索再…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：RouterQueryEngine：根据问题类型路由到不同的检索策略"

[[scenes]]
id = "s06"
narration_index = 6
title = "LlamaIndex的局限"
purpose = "concept"
visual_type = "code-terminal"
layout = "code"
key_points = ["LlamaIndex的局限", "和LangChain类似，抽象层会隐藏底层细节", "当你需要精细控制Milvus的索引参数、搜索参数、或者做复杂的混合检索时，框架的封…"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：LlamaIndex的局限"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：和LangChain类似，抽象层会隐藏底层细节"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：当你需要精细控制Milvus的索引参数、搜索参数、或者做复杂的混合检索时，框架的封…"

[[scenes]]
id = "s07"
narration_index = 7
title = "LangChain vs LlamaIndex怎么选"
purpose = "demo"
visual_type = "code-terminal"
layout = "code"
key_points = ["LangChain vs LlamaIndex怎么选", "如果你的重点是数据处理和检索质量，选LlamaIndex", "如果你的重点是链路编排和Agent，选LangChain"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：LangChain vs LlamaIndex怎么选"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：如果你的重点是数据处理和检索质量，选LlamaIndex"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：如果你的重点是链路编排和Agent，选LangChain"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "LlamaIndex是数据索引专家，擅长把各种数据源高效接入RAG", "和Milvus配合，几行代码就能搭建高质量的检索系统"]
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
description = "用动态图解展开：LlamaIndex是数据索引专家，擅长把各种数据源高效接入RAG"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：和Milvus配合，几行代码就能搭建高质量的检索系统"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
