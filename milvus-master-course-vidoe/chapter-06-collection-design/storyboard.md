# Chapter 06 Collection 设计视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/06-Collection设计.md`
- 核心问题：用可视化方式讲清《06 Collection 设计》中的关键概念、工程流程与选择依据
- 场景数量：7 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "06"
title = "Collection 设计"
source_doc = "../../milvus-master-course/docs/06-Collection设计.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "这一章聊Collection设计：主键怎么选、字段怎么…"
purpose = "hook"
visual_type = "learning-map"
layout = "full"
key_points = ["上一章我们学了pymilvus的API，但API只是工具，设计才是灵魂", "这一章聊Collection设计：主键怎么选、字段怎么规划、动态字段什么时候用、多…", "设计得好，后面省无数麻烦"]
components = ["chapter-map", "learning-goals", "progress-path"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "chapter-map"
description = "建立场景主题：上一章我们学了pymilvus的API，但API只是工具，设计才是灵魂"

[[scenes.beats]]
at = 0.36
action = "connect"
target = "learning-goals"
description = "用动态图解展开：这一章聊Collection设计：主键怎么选、字段怎么规划、动态字段什么时候用、多…"

[[scenes.beats]]
at = 0.72
action = "preview"
target = "progress-path"
description = "突出结论并承接下一段：设计得好，后面省无数麻烦"

[[scenes]]
id = "s02"
narration_index = 2
title = "主键"
purpose = "demo"
visual_type = "code-terminal"
layout = "code"
key_points = ["主键", "主键决定了upsert和delete的行为", "推荐用VARCHAR加业务ID，比如内容的SHA256哈希前32位"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：主键"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：主键决定了upsert和delete的行为"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：推荐用VARCHAR加业务ID，比如内容的SHA256哈希前32位"

[[scenes]]
id = "s03"
narration_index = 3
title = "主键定了，接下来规划字段"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["主键定了，接下来规划字段", "字段分四层来想", "检索层：向量字段，决定搜什么"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：主键定了，接下来规划字段"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：字段分四层来想"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：检索层：向量字段，决定搜什么"

[[scenes]]
id = "s04"
narration_index = 4
title = "一个常见问题：要不要用多向量字段"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["一个常见问题：要不要用多向量字段", "比如一个Collection里同时存title_embedding和body_em…", "答案是看场景"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：一个常见问题：要不要用多向量字段"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：比如一个Collection里同时存title_embedding和body_em…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：答案是看场景"

[[scenes]]
id = "s05"
narration_index = 5
title = "动态字段"
purpose = "concept"
visual_type = "code-terminal"
layout = "code"
key_points = ["动态字段", "enable_dynamic_field开了之后，可以写入Schema里没定义的字…", "动态键可以使用JSON路径索引加速，但显式字段仍然有更清晰的类型约束和索引管理"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：动态字段"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：enable_dynamic_field开了之后，可以写入Schema里没定义的字…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：动态键可以使用JSON路径索引加速，但显式字段仍然有更清晰的类型约束和索引管理"

[[scenes]]
id = "s06"
narration_index = 6
title = "聊多租户"
purpose = "concept"
visual_type = "cluster-search"
layout = "diagram"
key_points = ["最后聊多租户", "如果多个客户共用一个Milvus实例，怎么隔离数据", "三种方案"]
components = ["clusters", "centroids", "query-node", "selected-regions"]

[[scenes.beats]]
at = 0.00
action = "cluster"
target = "clusters"
description = "建立场景主题：最后聊多租户"

[[scenes.beats]]
at = 0.36
action = "probe"
target = "centroids"
description = "用动态图解展开：如果多个客户共用一个Milvus实例，怎么隔离数据"

[[scenes.beats]]
at = 0.72
action = "select"
target = "query-node"
description = "突出结论并承接下一段：三种方案"

[[scenes]]
id = "s07"
narration_index = 7
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "Collection设计的核心是回答五个问题：搜什么、过滤什么、展示什么、怎么更新…", "想清楚这五个问题再建表，比建完再改省十倍功夫"]
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
description = "用动态图解展开：Collection设计的核心是回答五个问题：搜什么、过滤什么、展示什么、怎么更新…"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：想清楚这五个问题再建表，比建完再改省十倍功夫"
```

## 人工检查

- [x] 7 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
