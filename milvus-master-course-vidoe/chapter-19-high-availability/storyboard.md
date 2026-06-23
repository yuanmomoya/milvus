# Chapter 19 Milvus 高可用设计视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/19-Milvus高可用设计.md`
- 核心问题：用可视化方式讲清《19 Milvus 高可用设计》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "19"
title = "Milvus 高可用设计"
source_doc = "../../milvus-master-course/docs/19-Milvus高可用设计.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "某个节点挂了，服务还能不能用"
purpose = "hook"
visual_type = "learning-map"
layout = "full"
key_points = ["上一章我们部署了集群，但集群不等于高可用", "某个节点挂了，服务还能不能用", "数据会不会丢"]
components = ["chapter-map", "learning-goals", "progress-path"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "chapter-map"
description = "建立场景主题：上一章我们部署了集群，但集群不等于高可用"

[[scenes.beats]]
at = 0.36
action = "connect"
target = "learning-goals"
description = "用动态图解展开：某个节点挂了，服务还能不能用"

[[scenes.beats]]
at = 0.72
action = "preview"
target = "progress-path"
description = "突出结论并承接下一段：数据会不会丢"

[[scenes]]
id = "s02"
narration_index = 2
title = "先看最关键的QueryNode"
purpose = "diagnosis"
visual_type = "error-diagnosis"
layout = "diagram"
key_points = ["先看最关键的QueryNode", "QueryNode挂了，它负责的Segment就搜不到了", "但如果配置了多副本，其他副本的QueryNode还能继续服务"]
components = ["symptom-card", "diagnosis-tree", "fix-checklist"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "symptom-card"
description = "建立场景主题：先看最关键的QueryNode"

[[scenes.beats]]
at = 0.36
action = "trace"
target = "diagnosis-tree"
description = "用动态图解展开：QueryNode挂了，它负责的Segment就搜不到了"

[[scenes.beats]]
at = 0.72
action = "resolve"
target = "fix-checklist"
description = "突出结论并承接下一段：但如果配置了多副本，其他副本的QueryNode还能继续服务"

[[scenes]]
id = "s03"
narration_index = 3
title = "Streaming Node故障会影响它负责的流式写入"
purpose = "diagnosis"
visual_type = "error-diagnosis"
layout = "diagram"
key_points = ["Streaming Node故障会影响它负责的流式写入", "只要WAL仍然可靠，未处理事件可以在任务重新分配后重放，但是否出现短暂失败以及恢复…"]
components = ["symptom-card", "diagnosis-tree", "fix-checklist"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "symptom-card"
description = "建立场景主题：Streaming Node故障会影响它负责的流式写入"

[[scenes.beats]]
at = 0.36
action = "trace"
target = "diagnosis-tree"
description = "用动态图解展开：只要WAL仍然可靠，未处理事件可以在任务重新分配后重放，但是否出现短暂失败以及恢复…"

[[scenes.beats]]
at = 0.72
action = "resolve"
target = "fix-checklist"
description = "突出结论并承接下一段：只要WAL仍然可靠，未处理事件可以在任务重新分配后重放，但是否出现短暂失败以及恢复…"

[[scenes]]
id = "s04"
narration_index = 4
title = "Proxy挂了影响连接"
purpose = "diagnosis"
visual_type = "error-diagnosis"
layout = "diagram"
key_points = ["Proxy挂了影响连接", "如果只有一个Proxy，所有客户端连接都会断", "所以生产环境至少部署两个Proxy，前面加负载均衡器"]
components = ["symptom-card", "diagnosis-tree", "fix-checklist"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "symptom-card"
description = "建立场景主题：Proxy挂了影响连接"

[[scenes.beats]]
at = 0.36
action = "trace"
target = "diagnosis-tree"
description = "用动态图解展开：如果只有一个Proxy，所有客户端连接都会断"

[[scenes.beats]]
at = 0.72
action = "resolve"
target = "fix-checklist"
description = "突出结论并承接下一段：所以生产环境至少部署两个Proxy，前面加负载均衡器"

[[scenes]]
id = "s05"
narration_index = 5
title = "Coord系列挂了影响调度"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["Coord系列挂了影响调度", "RootCoord挂了不能创建Collection，DataCoord挂了不能调度…", "但已经在运行的搜索和写入不受影响"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：Coord系列挂了影响调度"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：RootCoord挂了不能创建Collection，DataCoord挂了不能调度…"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：但已经在运行的搜索和写入不受影响"

[[scenes]]
id = "s06"
narration_index = 6
title = "基础设施的高可用更关键"
purpose = "diagnosis"
visual_type = "error-diagnosis"
layout = "diagram"
key_points = ["基础设施的高可用更关键", "etcd失去多数派后，元数据和调度操作会失败，因此生产环境通常使用三节点或更多奇数…", "对象存储故障会影响持久化、加载和故障恢复，不能只假设内存中的数据永远可搜"]
components = ["symptom-card", "diagnosis-tree", "fix-checklist"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "symptom-card"
description = "建立场景主题：基础设施的高可用更关键"

[[scenes.beats]]
at = 0.36
action = "trace"
target = "diagnosis-tree"
description = "用动态图解展开：etcd失去多数派后，元数据和调度操作会失败，因此生产环境通常使用三节点或更多奇数…"

[[scenes.beats]]
at = 0.72
action = "resolve"
target = "fix-checklist"
description = "突出结论并承接下一段：对象存储故障会影响持久化、加载和故障恢复，不能只假设内存中的数据永远可搜"

[[scenes]]
id = "s07"
narration_index = 7
title = "怎么设计高可用架构"
purpose = "diagnosis"
visual_type = "error-diagnosis"
layout = "diagram"
key_points = ["怎么设计高可用架构", "几个原则", "QueryNode至少两副本，保证搜索不中断"]
components = ["symptom-card", "diagnosis-tree", "fix-checklist"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "symptom-card"
description = "建立场景主题：怎么设计高可用架构"

[[scenes.beats]]
at = 0.36
action = "trace"
target = "diagnosis-tree"
description = "用动态图解展开：几个原则"

[[scenes.beats]]
at = 0.72
action = "resolve"
target = "fix-checklist"
description = "突出结论并承接下一段：QueryNode至少两副本，保证搜索不中断"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "Milvus高可用的核心是冗余和快速恢复", "QueryNode多副本保搜索，Proxy多实例保连接，基础设施三副本保数据"]
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
description = "用动态图解展开：Milvus高可用的核心是冗余和快速恢复"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：QueryNode多副本保搜索，Proxy多实例保连接，基础设施三副本保数据"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
