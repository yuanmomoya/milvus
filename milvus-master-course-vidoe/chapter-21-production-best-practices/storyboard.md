# Chapter 21 Milvus 生产最佳实践视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/21-Milvus生产最佳实践.md`
- 核心问题：用可视化方式讲清《21 Milvus 生产最佳实践》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "21"
title = "Milvus 生产最佳实践"
source_doc = "../../milvus-master-course/docs/21-Milvus生产最佳实践.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "前面二十章从基础到集群，知识点很多"
purpose = "hook"
visual_type = "learning-map"
layout = "full"
key_points = ["前面二十章从基础到集群，知识点很多", "这一章做一个生产最佳实践的总结清单", "不讲新概念，只讲\"上线前必须检查的事项\""]
components = ["chapter-map", "learning-goals", "progress-path"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "chapter-map"
description = "建立场景主题：前面二十章从基础到集群，知识点很多"

[[scenes.beats]]
at = 0.36
action = "connect"
target = "learning-goals"
description = "用动态图解展开：这一章做一个生产最佳实践的总结清单"

[[scenes.beats]]
at = 0.72
action = "preview"
target = "progress-path"
description = "突出结论并承接下一段：不讲新概念，只讲\"上线前必须检查的事项\""

[[scenes]]
id = "s02"
narration_index = 2
title = "第一类：Schema设计"
purpose = "concept"
visual_type = "code-terminal"
layout = "code"
key_points = ["第一类：Schema设计", "主键用VARCHAR加内容哈希，支持upsert幂等", "高频过滤字段显式定义并建INVERTED索引"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：第一类：Schema设计"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：主键用VARCHAR加内容哈希，支持upsert幂等"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：高频过滤字段显式定义并建INVERTED索引"

[[scenes]]
id = "s03"
narration_index = 3
title = "第二类：索引选择"
purpose = "comparison"
visual_type = "graph-search"
layout = "diagram"
key_points = ["第二类：索引选择", "中小规模首选HNSW，M设16，efConstruction设200", "内存紧张用IVF_SQ8或IVF_PQ"]
components = ["graph-layers", "search-route", "candidate-nodes"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "graph-layers"
description = "建立场景主题：第二类：索引选择"

[[scenes.beats]]
at = 0.36
action = "traverse"
target = "search-route"
description = "用动态图解展开：中小规模首选HNSW，M设16，efConstruction设200"

[[scenes.beats]]
at = 0.72
action = "arrive"
target = "candidate-nodes"
description = "突出结论并承接下一段：内存紧张用IVF_SQ8或IVF_PQ"

[[scenes]]
id = "s04"
narration_index = 4
title = "第三类：写入规范"
purpose = "concept"
visual_type = "code-terminal"
layout = "code"
key_points = ["第三类：写入规范", "batch_size设1000到5000", "用upsert不用insert"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：第三类：写入规范"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：batch_size设1000到5000"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：用upsert不用insert"

[[scenes]]
id = "s05"
narration_index = 5
title = "第四类：搜索规范"
purpose = "diagnosis"
visual_type = "error-diagnosis"
layout = "diagram"
key_points = ["第四类：搜索规范", "output_fields只返回必要字段", "TopK不要设过大"]
components = ["symptom-card", "diagnosis-tree", "fix-checklist"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "symptom-card"
description = "建立场景主题：第四类：搜索规范"

[[scenes.beats]]
at = 0.36
action = "trace"
target = "diagnosis-tree"
description = "用动态图解展开：output_fields只返回必要字段"

[[scenes.beats]]
at = 0.72
action = "resolve"
target = "fix-checklist"
description = "突出结论并承接下一段：TopK不要设过大"

[[scenes]]
id = "s06"
narration_index = 6
title = "第五类：运维规范"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["第五类：运维规范", "开启鉴权，不要用默认密码", "配置健康检查和自动重启"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：第五类：运维规范"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：开启鉴权，不要用默认密码"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：配置健康检查和自动重启"

[[scenes]]
id = "s07"
narration_index = 7
title = "第六类：安全规范"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["第六类：安全规范", "生产环境必须开authorizationEnabled", "SDK连接用token认证"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：第六类：安全规范"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：生产环境必须开authorizationEnabled"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：SDK连接用token认证"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "生产最佳实践不是一次性的事，是持续的纪律", "Schema设计决定上限，索引选择决定性能，写入规范决定稳定性，监控告警决定响应速度"]
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
description = "用动态图解展开：生产最佳实践不是一次性的事，是持续的纪律"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：Schema设计决定上限，索引选择决定性能，写入规范决定稳定性，监控告警决定响应速度"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
