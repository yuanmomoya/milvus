# Chapter 03 Milvus 快速开始视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/03-Milvus快速开始.md`
- 核心问题：用可视化方式讲清《03 Milvus 快速开始》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "03"
title = "Milvus 快速开始"
source_doc = "../../milvus-master-course/docs/03-Milvus快速开始.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "前两章我们搞清楚了向量检索的原理和Milvus的架构"
purpose = "hook"
visual_type = "learning-map"
layout = "full"
key_points = ["前两章我们搞清楚了向量检索的原理和Milvus的架构", "原理再好，不跑起来都是纸上谈兵", "这一章我们动手：用五步把Milvus从零跑通——启动服务、连接、建表、写入、搜索"]
components = ["chapter-map", "learning-goals", "progress-path"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "chapter-map"
description = "建立场景主题：前两章我们搞清楚了向量检索的原理和Milvus的架构"

[[scenes.beats]]
at = 0.36
action = "connect"
target = "learning-goals"
description = "用动态图解展开：原理再好，不跑起来都是纸上谈兵"

[[scenes.beats]]
at = 0.72
action = "preview"
target = "progress-path"
description = "突出结论并承接下一段：这一章我们动手：用五步把Milvus从零跑通——启动服务、连接、建表、写入、搜索"

[[scenes]]
id = "s02"
narration_index = 2
title = "第一步，启动Milvus"
purpose = "demo"
visual_type = "architecture"
layout = "diagram"
key_points = ["第一步，启动Milvus", "项目里已经准备好了Docker Compose文件，一条命令就能拉起Milvus…", "docker compose up -d，等三十秒，curl一下健康检查接口返回O…"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：第一步，启动Milvus"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：项目里已经准备好了Docker Compose文件，一条命令就能拉起Milvus…"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：docker compose up -d，等三十秒，curl一下健康检查接口返回O…"

[[scenes]]
id = "s03"
narration_index = 3
title = "服务跑起来了，接下来用Python连上它"
purpose = "demo"
visual_type = "architecture"
layout = "diagram"
key_points = ["服务跑起来了，接下来用Python连上它", "pymilvus提供了MilvusClient这个高层API，三行代码就能建立连接", "传入地址localhost 19530，调用list_collections验证一…"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：服务跑起来了，接下来用Python连上它"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：pymilvus提供了MilvusClient这个高层API，三行代码就能建立连接"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：传入地址localhost 19530，调用list_collections验证一…"

[[scenes]]
id = "s04"
narration_index = 4
title = "连上了，下一步是建表——在Milvus里叫Collec…"
purpose = "comparison"
visual_type = "graph-search"
layout = "diagram"
key_points = ["连上了，下一步是建表——在Milvus里叫Collection", "你需要定义Schema：主键字段、文本字段、还有最关键的向量字段", "向量字段要指定维度，必须和你后面用的Embedding模型输出一致"]
components = ["graph-layers", "search-route", "candidate-nodes"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "graph-layers"
description = "建立场景主题：连上了，下一步是建表——在Milvus里叫Collection"

[[scenes.beats]]
at = 0.36
action = "traverse"
target = "search-route"
description = "用动态图解展开：你需要定义Schema：主键字段、文本字段、还有最关键的向量字段"

[[scenes.beats]]
at = 0.72
action = "arrive"
target = "candidate-nodes"
description = "突出结论并承接下一段：向量字段要指定维度，必须和你后面用的Embedding模型输出一致"

[[scenes]]
id = "s05"
narration_index = 5
title = "表建好了，但数据还是原始文本，Milvus存的是向量"
purpose = "demo"
visual_type = "pipeline"
layout = "diagram"
key_points = ["表建好了，但数据还是原始文本，Milvus存的是向量", "所以需要一个Embedding模型把文本变成向量", "我们用bge-small-zh，一个针对中文检索优化的模型，输出512维向量"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：表建好了，但数据还是原始文本，Milvus存的是向量"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：所以需要一个Embedding模型把文本变成向量"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：我们用bge-small-zh，一个针对中文检索优化的模型，输出512维向量"

[[scenes]]
id = "s06"
narration_index = 6
title = "向量有了，写入Milvus"
purpose = "concept"
visual_type = "code-terminal"
layout = "code"
key_points = ["向量有了，写入Milvus", "用upsert而不是insert——好处是相同主键的数据会自动覆盖，天然幂等", "upsert返回成功意味着数据进入了WAL"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：向量有了，写入Milvus"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：用upsert而不是insert——好处是相同主键的数据会自动覆盖，天然幂等"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：upsert返回成功意味着数据进入了WAL"

[[scenes]]
id = "s07"
narration_index = 7
title = "数据写进去了，来搜一下"
purpose = "demo"
visual_type = "pipeline"
layout = "diagram"
key_points = ["数据写进去了，来搜一下", "把用户的问题也用同一个模型编码成向量，然后调用search", "Milvus返回TopK个最相似的结果，每条带一个距离或相似度分数"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：数据写进去了，来搜一下"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：把用户的问题也用同一个模型编码成向量，然后调用search"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：Milvus返回TopK个最相似的结果，每条带一个距离或相似度分数"

[[scenes]]
id = "s08"
narration_index = 8
title = "回顾一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，回顾一下", "五步闭环：启动、连接、建表、写入、搜索", "这就是Milvus的最小可用路径"]
components = ["knowledge-map", "chapter-progress", "next-chapter-card"]

[[scenes.beats]]
at = 0.00
action = "assemble"
target = "knowledge-map"
description = "建立场景主题：好，回顾一下"

[[scenes.beats]]
at = 0.36
action = "recap"
target = "chapter-progress"
description = "用动态图解展开：五步闭环：启动、连接、建表、写入、搜索"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：这就是Milvus的最小可用路径"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
