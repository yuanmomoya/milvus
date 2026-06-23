# Chapter 27 Agent 结合 Milvus视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/27-Agent结合Milvus.md`
- 核心问题：用可视化方式讲清《27 Agent 结合 Milvus》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "27"
title = "Agent 结合 Milvus"
source_doc = "../../milvus-master-course/docs/27-Agent结合Milvus.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "前面的RAG系统有个假设：每次用户提问都需要检索"
purpose = "hook"
visual_type = "hook-comparison"
layout = "split"
key_points = ["前面的RAG系统有个假设：每次用户提问都需要检索", "但实际上不是所有问题都需要查知识库", "\"你好\"不需要检索，\"今天天气怎么样\"也不需要"]
components = ["question-card", "before-after-panels", "conflict-highlight"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "question-card"
description = "建立场景主题：前面的RAG系统有个假设：每次用户提问都需要检索"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "before-after-panels"
description = "用动态图解展开：但实际上不是所有问题都需要查知识库"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "conflict-highlight"
description = "突出结论并承接下一段：\"你好\"不需要检索，\"今天天气怎么样\"也不需要"

[[scenes]]
id = "s02"
narration_index = 2
title = "Agent的核心概念是Tool Calling"
purpose = "demo"
visual_type = "pipeline"
layout = "diagram"
key_points = ["Agent的核心概念是Tool Calling", "你给大模型定义一组工具，比如search_knowledge_base、get_u…", "模型根据用户问题自己决定调用哪个工具、传什么参数"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：Agent的核心概念是Tool Calling"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：你给大模型定义一组工具，比如search_knowledge_base、get_u…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：模型根据用户问题自己决定调用哪个工具、传什么参数"

[[scenes]]
id = "s03"
narration_index = 3
title = "怎么把Milvus包装成Agent工具"
purpose = "demo"
visual_type = "pipeline"
layout = "diagram"
key_points = ["怎么把Milvus包装成Agent工具", "定义一个函数，接收查询文本和可选的过滤条件，内部调用Milvus的search，返…", "然后把这个函数注册为LLM的tool"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：怎么把Milvus包装成Agent工具"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：定义一个函数，接收查询文本和可选的过滤条件，内部调用Milvus的search，返…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：然后把这个函数注册为LLM的tool"

[[scenes]]
id = "s04"
narration_index = 4
title = "Agent比纯RAG强在哪"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["Agent比纯RAG强在哪", "第一，多步推理", "复杂问题可能需要多次检索：先搜A的信息，再搜B的信息，最后综合回答"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：Agent比纯RAG强在哪"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：第一，多步推理"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：复杂问题可能需要多次检索：先搜A的信息，再搜B的信息，最后综合回答"

[[scenes]]
id = "s05"
narration_index = 5
title = "实现Agent有几种方式"
purpose = "demo"
visual_type = "code-terminal"
layout = "code"
key_points = ["实现Agent有几种方式", "最简单的是用OpenAI的Function Calling API：定义tools…", "LangChain和LlamaIndex都封装了Agent框架，提供了更高层的抽象"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：实现Agent有几种方式"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：最简单的是用OpenAI的Function Calling API：定义tools…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：LangChain和LlamaIndex都封装了Agent框架，提供了更高层的抽象"

[[scenes]]
id = "s06"
narration_index = 6
title = "Agent的挑战"
purpose = "demo"
visual_type = "dashboard"
layout = "dashboard"
key_points = ["Agent的挑战", "第一，延迟增加", "每次工具调用都是一次LLM请求加一次Milvus搜索，多步推理延迟叠加"]
components = ["metric-cards", "trend-chart", "threshold-line", "tradeoff-control"]

[[scenes.beats]]
at = 0.00
action = "reveal"
target = "metric-cards"
description = "建立场景主题：Agent的挑战"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "trend-chart"
description = "用动态图解展开：第一，延迟增加"

[[scenes.beats]]
at = 0.72
action = "balance"
target = "threshold-line"
description = "突出结论并承接下一段：每次工具调用都是一次LLM请求加一次Milvus搜索，多步推理延迟叠加"

[[scenes]]
id = "s07"
narration_index = 7
title = "一个实用的模式是ReAct：Reasoning加Act…"
purpose = "demo"
visual_type = "pipeline"
layout = "diagram"
key_points = ["一个实用的模式是ReAct：Reasoning加Acting", "模型先思考需要什么信息，再决定调用什么工具，看到结果后再思考下一步", "这个思考过程对用户可见，增加了透明度和可调试性"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：一个实用的模式是ReAct：Reasoning加Acting"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：模型先思考需要什么信息，再决定调用什么工具，看到结果后再思考下一步"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：这个思考过程对用户可见，增加了透明度和可调试性"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "Agent让AI从被动检索变成主动决策", "Milvus作为Agent的一个工具，被按需调用"]
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
description = "用动态图解展开：Agent让AI从被动检索变成主动决策"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：Milvus作为Agent的一个工具，被按需调用"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
