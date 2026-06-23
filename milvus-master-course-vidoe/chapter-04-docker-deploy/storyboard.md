# Chapter 04 Docker 部署 Milvus视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/04-Docker部署Milvus.md`
- 核心问题：用可视化方式讲清《04 Docker 部署 Milvus》中的关键概念、工程流程与选择依据
- 场景数量：7 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "04"
title = "Docker 部署 Milvus"
source_doc = "../../milvus-master-course/docs/04-Docker部署Milvus.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "但生产环境不能靠默认值"
purpose = "hook"
visual_type = "learning-map"
layout = "full"
key_points = ["上一章我们五步跑通了Milvus，用的是默认配置", "但生产环境不能靠默认值", "这一章我们深入Docker Compose部署：搞清楚三个服务各自干什么、端口怎么…"]
components = ["chapter-map", "learning-goals", "progress-path"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "chapter-map"
description = "建立场景主题：上一章我们五步跑通了Milvus，用的是默认配置"

[[scenes.beats]]
at = 0.36
action = "connect"
target = "learning-goals"
description = "用动态图解展开：但生产环境不能靠默认值"

[[scenes.beats]]
at = 0.72
action = "preview"
target = "progress-path"
description = "突出结论并承接下一段：这一章我们深入Docker Compose部署：搞清楚三个服务各自干什么、端口怎么…"

[[scenes]]
id = "s02"
narration_index = 2
title = "先看Docker Compose里的三个服务"
purpose = "concept"
visual_type = "architecture"
layout = "diagram"
key_points = ["先看Docker Compose里的三个服务", "etcd负责存元数据——Collection的Schema、Segment的位置信…", "MinIO是对象存储，存的是真正的向量数据文件：Binlog、DeltaLog和索…"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：先看Docker Compose里的三个服务"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：etcd负责存元数据——Collection的Schema、Segment的位置信…"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：MinIO是对象存储，存的是真正的向量数据文件：Binlog、DeltaLog和索…"

[[scenes]]
id = "s03"
narration_index = 3
title = "端口规划很简单"
purpose = "demo"
visual_type = "architecture"
layout = "diagram"
key_points = ["端口规划很简单", "19530是SDK连接端口，你的Python代码连这个", "9091是健康检查和Prometheus指标端口，运维用"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：端口规划很简单"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：19530是SDK连接端口，你的Python代码连这个"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：9091是健康检查和Prometheus指标端口，运维用"

[[scenes]]
id = "s04"
narration_index = 4
title = "光靠环境变量不够精细，Milvus还支持配置文件覆盖"
purpose = "concept"
visual_type = "error-diagnosis"
layout = "diagram"
key_points = ["光靠环境变量不够精细，Milvus还支持配置文件覆盖", "把milvus.yaml挂载到容器的configs目录，就能控制日志级别、鉴权开关…", "开发环境关鉴权、调debug日志"]
components = ["symptom-card", "diagnosis-tree", "fix-checklist"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "symptom-card"
description = "建立场景主题：光靠环境变量不够精细，Milvus还支持配置文件覆盖"

[[scenes.beats]]
at = 0.36
action = "trace"
target = "diagnosis-tree"
description = "用动态图解展开：把milvus.yaml挂载到容器的configs目录，就能控制日志级别、鉴权开关…"

[[scenes.beats]]
at = 0.72
action = "resolve"
target = "fix-checklist"
description = "突出结论并承接下一段：开发环境关鉴权、调debug日志"

[[scenes]]
id = "s05"
narration_index = 5
title = "跨平台部署有几个坑要注意"
purpose = "diagnosis"
visual_type = "architecture"
layout = "diagram"
key_points = ["跨平台部署有几个坑要注意", "macOS和Windows上的Docker Desktop要检查实际分配给虚拟机的…", "Windows优先使用Docker Desktop当前推荐的WSL2后端"]
components = ["service-nodes", "request-path", "storage-layer"]

[[scenes.beats]]
at = 0.00
action = "build"
target = "service-nodes"
description = "建立场景主题：跨平台部署有几个坑要注意"

[[scenes.beats]]
at = 0.36
action = "route"
target = "request-path"
description = "用动态图解展开：macOS和Windows上的Docker Desktop要检查实际分配给虚拟机的…"

[[scenes.beats]]
at = 0.72
action = "focus"
target = "storage-layer"
description = "突出结论并承接下一段：Windows优先使用Docker Desktop当前推荐的WSL2后端"

[[scenes]]
id = "s06"
narration_index = 6
title = "说说启动失败怎么排查"
purpose = "diagnosis"
visual_type = "error-diagnosis"
layout = "diagram"
key_points = ["最后说说启动失败怎么排查", "最常见的是Milvus反复重启——通常是etcd没就绪就启动了，检查depends…", "端口被占用用lsof查"]
components = ["symptom-card", "diagnosis-tree", "fix-checklist"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "symptom-card"
description = "建立场景主题：最后说说启动失败怎么排查"

[[scenes.beats]]
at = 0.36
action = "trace"
target = "diagnosis-tree"
description = "用动态图解展开：最常见的是Milvus反复重启——通常是etcd没就绪就启动了，检查depends…"

[[scenes.beats]]
at = 0.72
action = "resolve"
target = "fix-checklist"
description = "突出结论并承接下一段：端口被占用用lsof查"

[[scenes]]
id = "s07"
narration_index = 7
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "Docker部署的核心是三件事：服务依赖顺序、端口和数据卷规划、配置文件覆盖", "掌握了这些，本地开发环境就稳了"]
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
description = "用动态图解展开：Docker部署的核心是三件事：服务依赖顺序、端口和数据卷规划、配置文件覆盖"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：掌握了这些，本地开发环境就稳了"
```

## 人工检查

- [x] 7 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
