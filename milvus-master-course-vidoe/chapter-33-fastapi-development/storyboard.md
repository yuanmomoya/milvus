# Chapter 33 FastAPI 接口开发视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/33-FastAPI接口开发.md`
- 核心问题：用可视化方式讲清《33 FastAPI 接口开发》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "33"
title = "FastAPI 接口开发"
source_doc = "../../milvus-master-course/docs/33-FastAPI接口开发.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "前面我们一直在写检索逻辑，但检索系统最终要通过API暴…"
purpose = "hook"
visual_type = "learning-map"
layout = "full"
key_points = ["前面我们一直在写检索逻辑，但检索系统最终要通过API暴露给前端或其他服务", "这一章我们用FastAPI开发向量检索的API接口：路由设计、请求响应模型、异步处…"]
components = ["chapter-map", "learning-goals", "progress-path"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "chapter-map"
description = "建立场景主题：前面我们一直在写检索逻辑，但检索系统最终要通过API暴露给前端或其他服务"

[[scenes.beats]]
at = 0.36
action = "connect"
target = "learning-goals"
description = "用动态图解展开：这一章我们用FastAPI开发向量检索的API接口：路由设计、请求响应模型、异步处…"

[[scenes.beats]]
at = 0.72
action = "preview"
target = "progress-path"
description = "突出结论并承接下一段：这一章我们用FastAPI开发向量检索的API接口：路由设计、请求响应模型、异步处…"

[[scenes]]
id = "s02"
narration_index = 2
title = "FastAPI的优势是什么"
purpose = "demo"
visual_type = "code-terminal"
layout = "code"
key_points = ["FastAPI的优势是什么", "类型安全、自动文档、异步支持、性能好", "用Pydantic定义请求和响应模型，FastAPI自动做参数校验和文档生成"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：FastAPI的优势是什么"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：类型安全、自动文档、异步支持、性能好"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：用Pydantic定义请求和响应模型，FastAPI自动做参数校验和文档生成"

[[scenes]]
id = "s03"
narration_index = 3
title = "API路由设计"
purpose = "concept"
visual_type = "code-terminal"
layout = "code"
key_points = ["API路由设计", "核心接口通常有四个", "POST /documents：上传文档，切分编码入库"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：API路由设计"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：核心接口通常有四个"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：POST /documents：上传文档，切分编码入库"

[[scenes]]
id = "s04"
narration_index = 4
title = "请求响应模型用Pydantic定义"
purpose = "concept"
visual_type = "metric-comparison"
layout = "split"
key_points = ["请求响应模型用Pydantic定义", "SearchRequest包含query、top_k、filter等字段", "SearchResponse包含results列表，每条有id、text、scor…"]
components = ["comparison-cards", "tradeoff-axis", "decision-marker"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "comparison-cards"
description = "建立场景主题：请求响应模型用Pydantic定义"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "tradeoff-axis"
description = "用动态图解展开：SearchRequest包含query、top_k、filter等字段"

[[scenes.beats]]
at = 0.72
action = "decide"
target = "decision-marker"
description = "突出结论并承接下一段：SearchResponse包含results列表，每条有id、text、scor…"

[[scenes]]
id = "s05"
narration_index = 5
title = "异步处理是关键"
purpose = "demo"
visual_type = "pipeline"
layout = "diagram"
key_points = ["异步处理是关键", "Milvus的pymilvus客户端本身是同步的，但可以用asyncio.to_t…", "Embedding编码如果用GPU，也是同步阻塞的，同样需要包装"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：异步处理是关键"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：Milvus的pymilvus客户端本身是同步的，但可以用asyncio.to_t…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：Embedding编码如果用GPU，也是同步阻塞的，同样需要包装"

[[scenes]]
id = "s06"
narration_index = 6
title = "错误处理要分层"
purpose = "diagnosis"
visual_type = "error-diagnosis"
layout = "diagram"
key_points = ["错误处理要分层", "Milvus连接失败返回503 Service Unavailable", "Collection不存在返回404"]
components = ["symptom-card", "diagnosis-tree", "fix-checklist"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "symptom-card"
description = "建立场景主题：错误处理要分层"

[[scenes.beats]]
at = 0.36
action = "trace"
target = "diagnosis-tree"
description = "用动态图解展开：Milvus连接失败返回503 Service Unavailable"

[[scenes.beats]]
at = 0.72
action = "resolve"
target = "fix-checklist"
description = "突出结论并承接下一段：Collection不存在返回404"

[[scenes]]
id = "s07"
narration_index = 7
title = "性能优化几个点"
purpose = "concept"
visual_type = "code-terminal"
layout = "code"
key_points = ["性能优化几个点", "第一，Embedding模型启动时加载一次，用lifespan事件管理", "第二，MilvusClient也是启动时创建一次，全局复用"]
components = ["code-editor", "terminal-output", "callout-labels"]

[[scenes.beats]]
at = 0.00
action = "type"
target = "code-editor"
description = "建立场景主题：性能优化几个点"

[[scenes.beats]]
at = 0.36
action = "execute"
target = "terminal-output"
description = "用动态图解展开：第一，Embedding模型启动时加载一次，用lifespan事件管理"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "callout-labels"
description = "突出结论并承接下一段：第二，MilvusClient也是启动时创建一次，全局复用"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "FastAPI加Milvus是构建向量检索API的标准组合", "类型安全保证接口质量，异步处理保证并发性能，分层错误处理保证可维护性"]
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
description = "用动态图解展开：FastAPI加Milvus是构建向量检索API的标准组合"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：类型安全保证接口质量，异步处理保证并发性能，分层错误处理保证可维护性"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
