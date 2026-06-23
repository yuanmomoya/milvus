# Chapter 14 标量过滤 ScalarFilter视频分镜

## 课程定位

- 对应教程：`../../milvus-master-course/docs/14-标量过滤ScalarFilter.md`
- 核心问题：用可视化方式讲清《14 标量过滤 ScalarFilter》中的关键概念、工程流程与选择依据
- 场景数量：8 个 Scene，与旁白段落和 timing 一一对应

## 分镜数据

```toml
schema_version = 1
chapter = "14"
title = "标量过滤 ScalarFilter"
source_doc = "../../milvus-master-course/docs/14-标量过滤ScalarFilter.md"
narration_file = "narration.txt"
timing_file = "narration_timing.json"
renderer = "hyperframes"
motion_canvas = false

[[scenes]]
id = "s01"
narration_index = 1
title = "但很多时候，用户的需求不只是\"找相似的\"，还有\"找相似…"
purpose = "hook"
visual_type = "hook-comparison"
layout = "split"
key_points = ["上一章我们用混合检索解决了漏召回问题", "但很多时候，用户的需求不只是\"找相似的\"，还有\"找相似的且满足某些条件的\"", "比如：找和这篇文章语义相似的、但只要最近一周发布的、且分类是技术的"]
components = ["question-card", "before-after-panels", "conflict-highlight"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "question-card"
description = "建立场景主题：上一章我们用混合检索解决了漏召回问题"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "before-after-panels"
description = "用动态图解展开：但很多时候，用户的需求不只是\"找相似的\"，还有\"找相似的且满足某些条件的\""

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "conflict-highlight"
description = "突出结论并承接下一段：比如：找和这篇文章语义相似的、但只要最近一周发布的、且分类是技术的"

[[scenes]]
id = "s02"
narration_index = 2
title = "标量过滤的本质是在向量搜索的基础上加WHERE条件"
purpose = "concept"
visual_type = "metric-comparison"
layout = "split"
key_points = ["标量过滤的本质是在向量搜索的基础上加WHERE条件", "Milvus的search方法有个filter参数，传入一个表达式字符串，语法类似…", "支持比较运算、逻辑运算、IN、LIKE、JSON路径等"]
components = ["comparison-cards", "tradeoff-axis", "decision-marker"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "comparison-cards"
description = "建立场景主题：标量过滤的本质是在向量搜索的基础上加WHERE条件"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "tradeoff-axis"
description = "用动态图解展开：Milvus的search方法有个filter参数，传入一个表达式字符串，语法类似…"

[[scenes.beats]]
at = 0.72
action = "decide"
target = "decision-marker"
description = "突出结论并承接下一段：支持比较运算、逻辑运算、IN、LIKE、JSON路径等"

[[scenes]]
id = "s03"
narration_index = 3
title = "常用的过滤表达式长这样"
purpose = "concept"
visual_type = "metric-comparison"
layout = "split"
key_points = ["常用的过滤表达式长这样", "等于：category == \"tech\"", "范围：created_at > 1700000000"]
components = ["comparison-cards", "tradeoff-axis", "decision-marker"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "comparison-cards"
description = "建立场景主题：常用的过滤表达式长这样"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "tradeoff-axis"
description = "用动态图解展开：等于：category == \"tech\""

[[scenes.beats]]
at = 0.72
action = "decide"
target = "decision-marker"
description = "突出结论并承接下一段：范围：created_at > 1700000000"

[[scenes]]
id = "s04"
narration_index = 4
title = "Milvus常规的标准过滤会先计算标量条件，再把得到的…"
purpose = "concept"
visual_type = "pipeline"
layout = "diagram"
key_points = ["Milvus常规的标准过滤会先计算标量条件，再把得到的位图交给向量搜索，避免不满足…", "对于表达式非常复杂、标量计算本身代价很高的场景，还可以使用迭代过滤，让系统分批取出…"]
components = ["flow-nodes", "data-packets", "result-card"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "flow-nodes"
description = "建立场景主题：Milvus常规的标准过滤会先计算标量条件，再把得到的位图交给向量搜索，避免不满足…"

[[scenes.beats]]
at = 0.36
action = "flow"
target = "data-packets"
description = "用动态图解展开：对于表达式非常复杂、标量计算本身代价很高的场景，还可以使用迭代过滤，让系统分批取出…"

[[scenes.beats]]
at = 0.72
action = "highlight"
target = "result-card"
description = "突出结论并承接下一段：对于表达式非常复杂、标量计算本身代价很高的场景，还可以使用迭代过滤，让系统分批取出…"

[[scenes]]
id = "s05"
narration_index = 5
title = "标准过滤适合大多数表达式，但复杂JSON或大量字符串条…"
purpose = "comparison"
visual_type = "dashboard"
layout = "dashboard"
key_points = ["标准过滤适合大多数表达式，但复杂JSON或大量字符串条件可能让标量过滤本身成为瓶颈", "迭代过滤可以减少一次性标量计算，却可能需要更多轮候选搜索", "选择哪种方式不能只看过滤比例，还要结合表达式复杂度、候选数量和实测延迟"]
components = ["metric-cards", "trend-chart", "threshold-line", "tradeoff-control"]

[[scenes.beats]]
at = 0.00
action = "reveal"
target = "metric-cards"
description = "建立场景主题：标准过滤适合大多数表达式，但复杂JSON或大量字符串条件可能让标量过滤本身成为瓶颈"

[[scenes.beats]]
at = 0.36
action = "measure"
target = "trend-chart"
description = "用动态图解展开：迭代过滤可以减少一次性标量计算，却可能需要更多轮候选搜索"

[[scenes.beats]]
at = 0.72
action = "balance"
target = "threshold-line"
description = "突出结论并承接下一段：选择哪种方式不能只看过滤比例，还要结合表达式复杂度、候选数量和实测延迟"

[[scenes]]
id = "s06"
narration_index = 6
title = "要让过滤快，关键是给高频过滤字段建标量索引"
purpose = "concept"
visual_type = "metric-comparison"
layout = "split"
key_points = ["要让过滤快，关键是给高频过滤字段建标量索引", "用INVERTED类型，适合等值和IN查询", "不建索引的字段也能过滤，但会全量扫描，数据量大时很慢"]
components = ["comparison-cards", "tradeoff-axis", "decision-marker"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "comparison-cards"
description = "建立场景主题：要让过滤快，关键是给高频过滤字段建标量索引"

[[scenes.beats]]
at = 0.36
action = "compare"
target = "tradeoff-axis"
description = "用动态图解展开：用INVERTED类型，适合等值和IN查询"

[[scenes.beats]]
at = 0.72
action = "decide"
target = "decision-marker"
description = "突出结论并承接下一段：不建索引的字段也能过滤，但会全量扫描，数据量大时很慢"

[[scenes]]
id = "s07"
narration_index = 7
title = "有个常见坑：过滤条件太严导致结果不够"
purpose = "diagnosis"
visual_type = "error-diagnosis"
layout = "diagram"
key_points = ["有个常见坑：过滤条件太严导致结果不够", "比如你要TopK等于10，但满足条件的数据只有3条", "这时候Milvus会返回3条，不会报错但结果不完整"]
components = ["symptom-card", "diagnosis-tree", "fix-checklist"]

[[scenes.beats]]
at = 0.00
action = "show"
target = "symptom-card"
description = "建立场景主题：有个常见坑：过滤条件太严导致结果不够"

[[scenes.beats]]
at = 0.36
action = "trace"
target = "diagnosis-tree"
description = "用动态图解展开：比如你要TopK等于10，但满足条件的数据只有3条"

[[scenes.beats]]
at = 0.72
action = "resolve"
target = "fix-checklist"
description = "突出结论并承接下一段：这时候Milvus会返回3条，不会报错但结果不完整"

[[scenes]]
id = "s08"
narration_index = 8
title = "总结一下"
purpose = "summary"
visual_type = "recap"
layout = "full"
key_points = ["好，总结一下", "标量过滤是向量搜索的精细化工具", "记住三点：高频字段建INVERTED索引、注意过滤比例对性能的影响、处理好结果不足…"]
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
description = "用动态图解展开：标量过滤是向量搜索的精细化工具"

[[scenes.beats]]
at = 0.72
action = "transition"
target = "next-chapter-card"
description = "突出结论并承接下一段：记住三点：高频字段建INVERTED索引、注意过滤比例对性能的影响、处理好结果不足…"
```

## 人工检查

- [x] 8 个 Scene 与旁白、timing 数量一致
- [x] 所有 Beat 使用 `0.0-1.0` 相对时间
- [x] 使用受控视觉类型和可复用组件
- [ ] 生成 HTML 后抽查每个场景的开头、中点和结尾
- [ ] 对本章涉及的版本、性能数字和经验阈值做最终人工复核
