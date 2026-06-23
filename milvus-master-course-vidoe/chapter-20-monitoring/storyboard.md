# Chapter 20 Milvus 监控体系视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/20-Milvus监控体系.md`
- 核心问题：用可视化方式讲清《20 Milvus 监控体系》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "20"
title = "Milvus 监控体系"
source_doc = "../../milvus-master-course/docs/20-Milvus监控体系.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "你得知道系统现在是不是健康的、哪里在变慢、什么时候该扩容"
purpose = "hook"
visual_type = "learning-map"
layout = "full"
key_points = ["上一章我们设计了高可用架构，但高可用不是部署完就完事了", "你得知道系统现在是不是健康的、哪里在变慢、什么时候该扩容", "这就是监控体系的作用"]
components = ["chapter-map", "learning-goals", "progress-path"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "chapter-map"
description = "建立场景主题：上一章我们设计了高可用架构，但高可用不是部署完就完事了"

[[scenes.beats]]
at = 0.36
action = "connect"
target = "learning-goals"
description = "用动态图解展开：你得知道系统现在是不是健康的、哪里在变慢、什么时候该扩容"

[[scenes.beats]]
at = 0.72
action = "preview"
target = "progress-path"
description = "突出结论并承接下一段：这就是监控体系的作用"

[[scenes]]
id = "s02"
narration_index = 2
title = "Milvus内置了Prometheus指标暴露"
purpose = "concept"
visual_type = "dashboard"
layout = "dashboard"
key_points = ["Milvus内置了Prometheus指标暴露", "每个组件的9091端口都有一个metrics接口，返回Prometheus格式的指…", "包括搜索延迟、写入吞吐、Segment数量、内存使用、索引构建进度等几百个指标"]
components = ["metric-cards", "trend-chart", "threshold-line", "tradeoff-control"]

[[scenes.beats]]
at = 0.00
action = "reveal"
target = "metric-cards"
description = "建立场景主题：Milvus内置了Prometheus指标暴露"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "trend-chart"
description = "用动态图解展开：每个组件的9091端口都有一个metrics接口，返回Prometheus格式的指…"

[[scenes.beats]]
at = 0.72
action = "balance"
target = "threshold-line"
description = "突出结论并承接下一段：包括搜索延迟、写入吞吐、Segment数量、内存使用、索引构建进度等几百个指标"

[[scenes]]
id = "s03"
narration_index = 3
title = "搭建监控的步骤很简单"
purpose = "concept"
visual_type = "code-terminal"
layout = "code"
key_points = ["搭建监控的步骤很简单", "第一步，部署Prometheus，配置scrape_configs指向Milvus…", "第二步，部署Grafana，导入Milvus官方的Dashboard模板"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：搭建监控的步骤很简单"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：第一步，部署Prometheus，配置scrape_configs指向Milvus…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：第二步，部署Grafana，导入Milvus官方的Dashboard模板"

[[scenes]]
id = "s04"
narration_index = 4
title = "最重要的几个指标"
purpose = "diagnosis"
visual_type = "error-diagnosis"
layout = "diagram"
key_points = ["最重要的几个指标", "搜索延迟P99：超过基线时检查QueryNode、过滤和索引参数", "写入吞吐：突然下降时沿客户端、Proxy、WAL、Streaming Node和对…"]
components = ["symptom-card", "diagnosis-tree", "fix-checklist"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "symptom-card"
description = "建立场景主题：最重要的几个指标"

[[scenes.beats]]
at = 0.36
action = "trace"
target = "diagnosis-tree"
description = "用动态图解展开：搜索延迟P99：超过基线时检查QueryNode、过滤和索引参数"

[[scenes.beats]]
at = 0.72
action = "resolve"
target = "fix-checklist"
description = "突出结论并承接下一段：写入吞吐：突然下降时沿客户端、Proxy、WAL、Streaming Node和对…"

[[scenes]]
id = "s05"
narration_index = 5
title = "告警规则怎么配"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["告警规则怎么配", "几个必配的", "搜索P99延迟超过500ms告警"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：告警规则怎么配"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：几个必配的"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：搜索P99延迟超过500ms告警"

[[scenes]]
id = "s06"
narration_index = 6
title = "除了指标监控，日志也很重要"
purpose = "diagnosis"
visual_type = "error-diagnosis"
layout = "diagram"
key_points = ["除了指标监控，日志也很重要", "Milvus的日志级别可以动态调整", "正常运行用info级别，排查问题时临时调成debug"]
components = ["symptom-card", "diagnosis-tree", "fix-checklist"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "symptom-card"
description = "建立场景主题：除了指标监控，日志也很重要"

[[scenes.beats]]
at = 0.36
action = "trace"
target = "diagnosis-tree"
description = "用动态图解展开：Milvus的日志级别可以动态调整"

[[scenes.beats]]
at = 0.72
action = "resolve"
target = "fix-checklist"
description = "突出结论并承接下一段：正常运行用info级别，排查问题时临时调成debug"

[[scenes]]
id = "s07"
narration_index = 7
title = "监控的最终目标是容量规划"
purpose = "diagnosis"
visual_type = "error-diagnosis"
layout = "diagram"
key_points = ["监控的最终目标是容量规划", "通过历史指标趋势，预测什么时候需要扩容", "比如内存使用每周增长5%，那两个月后就会到上限"]
components = ["symptom-card", "diagnosis-tree", "fix-checklist"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "symptom-card"
description = "建立场景主题：监控的最终目标是容量规划"

[[scenes.beats]]
at = 0.36
action = "trace"
target = "diagnosis-tree"
description = "用动态图解展开：通过历史指标趋势，预测什么时候需要扩容"

[[scenes.beats]]
at = 0.72
action = "resolve"
target = "fix-checklist"
description = "突出结论并承接下一段：比如内存使用每周增长5%，那两个月后就会到上限"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "监控体系的三板斧：Prometheus采指标、Grafana看趋势、告警规则防故障", "部署简单但价值巨大——没有监控的生产系统就是在裸奔"]
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
description = "用动态图解展开：监控体系的三板斧：Prometheus采指标、Grafana看趋势、告警规则防故障"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：部署简单但价值巨大——没有监控的生产系统就是在裸奔"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
