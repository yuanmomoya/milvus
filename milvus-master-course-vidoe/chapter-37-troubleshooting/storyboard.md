# Chapter 37 问题排查与 Debug视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/37-问题排查与Debug.md`
- 核心问题：用可视化方式讲清《37 问题排查与 Debug》中的关键概念、工程流程与选择依据
- 场景数量：9 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "37"
title = "问题排查与 Debug"
source_doc = "../../milvus-master-course/docs/37-问题排查与Debug.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "系统跑着跑着突然出问题了：搜索变慢、写入报错、服务重启"
purpose = "hook"
visual_type = "hook-comparison"
layout = "split"
key_points = ["系统跑着跑着突然出问题了：搜索变慢、写入报错、服务重启", "这一章是问题排查指南：从现象到原因的排查思路、常用的诊断命令、以及典型问题的解决方案"]
components = ["question-card", "before-after-panels", "conflict-highlight"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "question-card"
description = "建立场景主题：系统跑着跑着突然出问题了：搜索变慢、写入报错、服务重启"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "before-after-panels"
description = "用动态图解展开：这一章是问题排查指南：从现象到原因的排查思路、常用的诊断命令、以及典型问题的解决方案"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "conflict-highlight"
description = "突出结论并承接下一段：这一章是问题排查指南：从现象到原因的排查思路、常用的诊断命令、以及典型问题的解决方案"

[[scenes]]
id = "s02"
narration_index = 2
title = "排查的第一步通常是确定问题在哪一层：客户端、网络、Pr…"
purpose = "diagnosis"
visual_type = "error-diagnosis"
layout = "diagram"
key_points = ["排查的第一步通常是确定问题在哪一层：客户端、网络、Proxy、后端组件还是依赖存储", "用curl检查healthz可以确认HTTP健康端点是否可达", "不通可能是网络、端口或服务问题，健康也不代表所有读写路径都正常，还要结合SDK错误…"]
components = ["symptom-card", "diagnosis-tree", "fix-checklist"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "symptom-card"
description = "建立场景主题：排查的第一步通常是确定问题在哪一层：客户端、网络、Proxy、后端组件还是依赖存储"

[[scenes.beats]]
at = 0.36
action = "trace"
target = "diagnosis-tree"
description = "用动态图解展开：用curl检查healthz可以确认HTTP健康端点是否可达"

[[scenes.beats]]
at = 0.72
action = "resolve"
target = "fix-checklist"
description = "突出结论并承接下一段：不通可能是网络、端口或服务问题，健康也不代表所有读写路径都正常，还要结合SDK错误…"

[[scenes]]
id = "s03"
narration_index = 3
title = "搜索变慢的排查流程"
purpose = "diagnosis"
visual_type = "error-diagnosis"
layout = "diagram"
key_points = ["搜索变慢的排查流程", "第一步，看监控：P99延迟是突然飙升还是逐渐上升", "突然飙升通常是某个事件触发的，比如大批量写入、Compaction、或者某个Que…"]
components = ["symptom-card", "diagnosis-tree", "fix-checklist"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "symptom-card"
description = "建立场景主题：搜索变慢的排查流程"

[[scenes.beats]]
at = 0.36
action = "trace"
target = "diagnosis-tree"
description = "用动态图解展开：第一步，看监控：P99延迟是突然飙升还是逐渐上升"

[[scenes.beats]]
at = 0.72
action = "resolve"
target = "fix-checklist"
description = "突出结论并承接下一段：突然飙升通常是某个事件触发的，比如大批量写入、Compaction、或者某个Que…"

[[scenes]]
id = "s04"
narration_index = 4
title = "第二步，看Segment状态"
purpose = "concept"
visual_type = "metric-comparison"
layout = "split"
key_points = ["第二步，看Segment状态", "用pymilvus的get_collection_stats查看Segment数量…", "如果有几千个小Segment，搜索合并开销大，需要Compaction"]
components = ["comparison-cards", "tradeoff-axis", "decision-marker"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "comparison-cards"
description = "建立场景主题：第二步，看Segment状态"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "tradeoff-axis"
description = "用动态图解展开：用pymilvus的get_collection_stats查看Segment数量…"

[[scenes.beats]]
at = 0.72
action = "decide"
target = "decision-marker"
description = "突出结论并承接下一段：如果有几千个小Segment，搜索合并开销大，需要Compaction"

[[scenes]]
id = "s05"
narration_index = 5
title = "写入报错的常见原因"
purpose = "diagnosis"
visual_type = "error-diagnosis"
layout = "diagram"
key_points = ["写入报错的常见原因", "维度不匹配：向量维度和Schema定义不一致，检查Embedding模型输出", "主键冲突：auto_id=False时主键重复，需要确认业务是拒绝重复还是用ups…"]
components = ["symptom-card", "diagnosis-tree", "fix-checklist"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "symptom-card"
description = "建立场景主题：写入报错的常见原因"

[[scenes.beats]]
at = 0.36
action = "trace"
target = "diagnosis-tree"
description = "用动态图解展开：维度不匹配：向量维度和Schema定义不一致，检查Embedding模型输出"

[[scenes.beats]]
at = 0.72
action = "resolve"
target = "fix-checklist"
description = "突出结论并承接下一段：主键冲突：auto_id=False时主键重复，需要确认业务是拒绝重复还是用ups…"

[[scenes]]
id = "s06"
narration_index = 6
title = "服务重启的排查"
purpose = "diagnosis"
visual_type = "error-diagnosis"
layout = "diagram"
key_points = ["服务重启的排查", "先看docker compose ps或kubectl get pods，确定哪个…", "然后看那个组件的日志，找到重启前的最后几行错误信息"]
components = ["symptom-card", "diagnosis-tree", "fix-checklist"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "symptom-card"
description = "建立场景主题：服务重启的排查"

[[scenes.beats]]
at = 0.36
action = "trace"
target = "diagnosis-tree"
description = "用动态图解展开：先看docker compose ps或kubectl get pods，确定哪个…"

[[scenes.beats]]
at = 0.72
action = "resolve"
target = "fix-checklist"
description = "突出结论并承接下一段：然后看那个组件的日志，找到重启前的最后几行错误信息"

[[scenes]]
id = "s07"
narration_index = 7
title = "几个实用的诊断命令"
purpose = "demo"
visual_type = "code-terminal"
layout = "code"
key_points = ["几个实用的诊断命令", "查看Collection加载状态：client.get_load_state", "查看索引构建进度：client.describe_index"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：几个实用的诊断命令"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：查看Collection加载状态：client.get_load_state"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：查看索引构建进度：client.describe_index"

[[scenes]]
id = "s08"
narration_index = 8
title = "一个排查清单"
purpose = "diagnosis"
visual_type = "error-diagnosis"
layout = "diagram"
key_points = ["一个排查清单", "搜索慢：检查索引是否建好、Segment是否过碎、ef/nprobe是否合理、ou…", "写入慢：检查batch_size、网络延迟、WAL积压、Streaming Nod…"]
components = ["symptom-card", "diagnosis-tree", "fix-checklist"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "symptom-card"
description = "建立场景主题：一个排查清单"

[[scenes.beats]]
at = 0.36
action = "trace"
target = "diagnosis-tree"
description = "用动态图解展开：搜索慢：检查索引是否建好、Segment是否过碎、ef/nprobe是否合理、ou…"

[[scenes.beats]]
at = 0.72
action = "resolve"
target = "fix-checklist"
description = "突出结论并承接下一段：写入慢：检查batch_size、网络延迟、WAL积压、Streaming Nod…"

[[scenes]]
id = "s09"
narration_index = 9
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "问题排查的核心思路是：分层定位、看监控、看日志、看状态", "大多数问题都能归结为：资源不足、配置错误、或者数据异常"]
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
description = "用动态图解展开：问题排查的核心思路是：分层定位、看监控、看日志、看状态"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：大多数问题都能归结为：资源不足、配置错误、或者数据异常"
```

## 人工检查

- [x] 9 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
