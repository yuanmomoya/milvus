# Chapter 34 构建完整 AI 搜索系统视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/34-构建完整AI搜索系统.md`
- 核心问题：用可视化方式讲清《34 构建完整 AI 搜索系统》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "34"
title = "构建完整 AI 搜索系统"
source_doc = "../../milvus-master-course/docs/34-构建完整AI搜索系统.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "前面三十三章我们学了各种组件和技术，这一章把它们整合成…"
purpose = "hook"
visual_type = "learning-map"
layout = "full"
key_points = ["前面三十三章我们学了各种组件和技术，这一章把它们整合成一个完整的AI搜索系统", "从架构设计到部署上线，走一遍完整的工程流程", "这不是Demo，是一个能真正服务用户的生产系统"]
components = ["chapter-map", "learning-goals", "progress-path"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "chapter-map"
description = "建立场景主题：前面三十三章我们学了各种组件和技术，这一章把它们整合成一个完整的AI搜索系统"

[[scenes.beats]]
at = 0.36
action = "connect"
target = "learning-goals"
description = "用动态图解展开：从架构设计到部署上线，走一遍完整的工程流程"

[[scenes.beats]]
at = 0.72
action = "preview"
target = "progress-path"
description = "突出结论并承接下一段：这不是Demo，是一个能真正服务用户的生产系统"

[[scenes]]
id = "s02"
narration_index = 2
title = "系统架构分四层"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["系统架构分四层", "接入层：Nginx做负载均衡和HTTPS终止，FastAPI处理请求", "检索层：Milvus做向量搜索，支持多路召回和混合检索"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：系统架构分四层"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：接入层：Nginx做负载均衡和HTTPS终止，FastAPI处理请求"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：检索层：Milvus做向量搜索，支持多路召回和混合检索"

[[scenes]]
id = "s03"
narration_index = 3
title = "数据处理管道是离线部分"
purpose = "concept"
visual_type = "code-terminal"
layout = "code"
key_points = ["数据处理管道是离线部分", "文档上传后进入队列，Worker异步处理：解析文档格式、按语义切分、用Embedd…", "处理完成后更新状态"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：数据处理管道是离线部分"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：文档上传后进入队列，Worker异步处理：解析文档格式、按语义切分、用Embedd…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：处理完成后更新状态"

[[scenes]]
id = "s04"
narration_index = 4
title = "在线检索流程"
purpose = "demo"
visual_type = "pipeline"
layout = "diagram"
key_points = ["在线检索流程", "用户提问进来，先做Query Rewrite生成多个查询变体", "然后多路并行检索：稠密向量搜索、稀疏向量搜索"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：在线检索流程"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：用户提问进来，先做Query Rewrite生成多个查询变体"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：然后多路并行检索：稠密向量搜索、稀疏向量搜索"

[[scenes]]
id = "s05"
narration_index = 5
title = "前端交互设计"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["前端交互设计", "搜索框支持自然语言输入", "结果展示分两部分：AI生成的答案在上方，引用的原始文档在下方"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：前端交互设计"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：搜索框支持自然语言输入"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：结果展示分两部分：AI生成的答案在上方，引用的原始文档在下方"

[[scenes]]
id = "s06"
narration_index = 6
title = "部署架构"
purpose = "demo"
visual_type = "architecture"
layout = "diagram"
key_points = ["部署架构", "FastAPI用Gunicorn加Uvicorn多Worker部署", "Milvus用Docker Compose或Kubernetes部署"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：部署架构"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：FastAPI用Gunicorn加Uvicorn多Worker部署"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：Milvus用Docker Compose或Kubernetes部署"

[[scenes]]
id = "s07"
narration_index = 7
title = "监控和运维"
purpose = "concept"
visual_type = "dashboard"
layout = "dashboard"
key_points = ["监控和运维", "接口层面：请求量、延迟P99、错误率", "检索层面：召回率、Milvus搜索延迟、Segment数量"]
components = ["metric-cards", "trend-chart", "threshold-line", "tradeoff-control"]

[[scenes.beats]]
at = 0.00
action = "reveal"
target = "metric-cards"
description = "建立场景主题：监控和运维"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "trend-chart"
description = "用动态图解展开：接口层面：请求量、延迟P99、错误率"

[[scenes.beats]]
at = 0.72
action = "balance"
target = "threshold-line"
description = "突出结论并承接下一段：检索层面：召回率、Milvus搜索延迟、Segment数量"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "完整的AI搜索系统是多个组件的协同：数据管道保证知识库新鲜，多路检索保证召回质量…", "下一章我们聊海量数据场景下的架构设计"]
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
description = "用动态图解展开：完整的AI搜索系统是多个组件的协同：数据管道保证知识库新鲜，多路检索保证召回质量…"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：下一章我们聊海量数据场景下的架构设计"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
