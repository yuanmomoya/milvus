# 02 Milvus整体架构

## 学习目标

学完本章后，你应该能够：

- 说清 Proxy、Coord、Worker Node、etcd、对象存储和 WAL 的职责。
- 画出 Milvus 写入流、查询流和索引构建流。
- 理解 Segment 生命周期、Flush、Compaction、WAL。
- 判断一个生产问题大概率发生在哪个组件。
- 区分单机 Standalone 和分布式 Cluster 的架构差异。

## 理论知识：形象化理解

Milvus 的架构可以想象成一个大型物流中心。Proxy 是前台接待，负责接收客户订单；Coord 系列像调度室，决定货物放在哪里、由谁处理、什么时候合并；Worker Node 像具体操作工位，真正执行流式写入、查询和建索引；etcd 是调度室墙上的总账本，MinIO/S3 是后方仓库，WAL 则是带流水号的传送带。

写入一条向量，不是把数据直接塞进某个单独文件就结束。它会先进入 WAL，像订单先贴上可追溯的流水号；Streaming Node 维护流式写入和 growing segment；Flush 后数据落到对象存储，Segment 被封存；IndexNode 再把它加工成适合快速搜索的索引。查询时，Proxy 会把请求拆给多个 QueryNode，拿到局部 TopK 后再归并成全局 TopK。

所以排查 Milvus 问题要像看物流链路一样定位：是前台接单慢、传送带堵了、仓库 IO 慢、调度表错了，还是搜索工位内存不够。架构图不是背组件名，而是建立“现象到组件”的映射。

## 总体架构

Milvus 采用计算存储分离和多组件协同架构。Proxy 接入请求，Coord 系列负责元数据和调度，Worker Node 负责具体执行，etcd 保存元数据，对象存储保存 Binlog/Index 文件，WAL 承载可靠的流式写入日志。下面按本课程使用的 Milvus 2.6 系列描述；其他版本的组件名称可能不同。

```mermaid
flowchart TB
    Client[SDK / REST / 应用服务] --> Proxy[Proxy]
    Proxy --> RootCoord[RootCoord]
    Proxy --> QueryCoord[QueryCoord]
    Proxy --> DataCoord[DataCoord]

    DataCoord --> StreamingNode[Streaming Node]
    QueryCoord --> QueryNode[QueryNode]
    DataCoord --> IndexNode[IndexNode]

    RootCoord --> Etcd[(etcd 元数据)]
    DataCoord --> Etcd
    QueryCoord --> Etcd
    StreamingNode --> WAL[(WAL / Streaming Storage)]
    StreamingNode --> Obj[(MinIO/S3 对象存储)]
    IndexNode --> Obj
    QueryNode --> Obj
```

## 组件职责

| 组件 | 职责 | 生产关注点 |
|---|---|---|
| Proxy | 接收客户端请求、鉴权、路由、参数校验 | QPS、连接数、请求错误率 |
| RootCoord | 管理数据库、Collection、字段、时间戳 | 元数据一致性、DDL 延迟 |
| DataCoord | 管理 Segment、Flush、Compaction | Segment 数量、Compaction 积压 |
| Streaming Node | 维护 WAL、流式写入和 growing Segment | 写入吞吐、WAL 延迟、Flush 延迟 |
| QueryCoord | 调度 QueryNode，管理 load/release | 加载耗时、副本分配 |
| QueryNode | 加载 Segment，执行搜索和查询 | 内存、搜索延迟、慢查询 |
| IndexNode | 构建向量/标量索引 | CPU/GPU、构建耗时 |
| etcd | 元数据和服务发现 | 备份、延迟、磁盘空间 |
| MinIO/S3 | Binlog、DeltaLog、Index 文件 | 容量、吞吐、可靠性 |
| WAL / Streaming Storage | 可靠写入日志和事件流 | 延迟、积压、持久化；实现取决于版本和部署配置 |

## 写入流程

```mermaid
sequenceDiagram
    participant App as 应用
    participant Proxy
    participant WAL
    participant StreamingNode
    participant Obj as MinIO/S3
    participant DataCoord
    participant QueryNode

    App->>Proxy: insert/upsert
    Proxy->>WAL: 追加写入日志
    WAL-->>Proxy: 达到一致性要求
    Proxy-->>App: 写入成功
    WAL->>StreamingNode: 流式消费
    StreamingNode->>StreamingNode: 维护 growing segment
    StreamingNode->>Obj: flush binlog
    StreamingNode->>DataCoord: 上报 sealed segment
    DataCoord->>QueryNode: 通知加载新 segment
```

写入成功、按一致性级别可见、索引构建完成是三个不同时间点。新写入数据可能先在 growing segment 中参与搜索，Flush 后成为 sealed segment，再由 IndexNode 构建索引。

## 查询流程

```mermaid
sequenceDiagram
    participant App as 应用
    participant Proxy
    participant QueryCoord
    participant QueryNode1 as QueryNode A
    participant QueryNode2 as QueryNode B

    App->>Proxy: search(collection, vector, filter)
    Proxy->>QueryCoord: 获取 shard/segment 分布
    Proxy->>QueryNode1: 搜索部分 Segment
    Proxy->>QueryNode2: 搜索部分 Segment
    QueryNode1-->>Proxy: 局部 TopK
    QueryNode2-->>Proxy: 局部 TopK
    Proxy->>Proxy: 归并、排序、回填字段
    Proxy-->>App: 全局 TopK
```

查询性能由多个因素共同决定：Collection 是否已 load，Segment 是否过碎，索引是否构建完成，过滤条件能否减少搜索范围，输出字段是否过大。

## Segment 生命周期

```mermaid
stateDiagram-v2
    [*] --> Growing: insert/upsert
    Growing --> Sealed: flush 或达到阈值
    Sealed --> Indexed: IndexNode 构建索引
    Indexed --> Loaded: QueryNode 加载
    Loaded --> Compacted: Compaction 合并/清理
    Compacted --> Loaded
    Loaded --> Released: release_collection
```

- Growing Segment：新写入数据，通常未构建索引，查询时可能暴力搜索。
- Sealed Segment：已封存，数据文件落到对象存储。
- Indexed Segment：索引构建完成，适合高性能 ANN 搜索。
- Compacted Segment：合并小 Segment 或清理删除数据后的新 Segment。

## Flush、Compaction、WAL

| 机制 | 解决的问题 | 过度使用的代价 |
|---|---|---|
| WAL | 写入可靠性和异步消费 | 消息积压会影响数据可见性 |
| Flush | 将内存数据持久化为 sealed segment | 频繁 flush 会产生大量小 Segment |
| Compaction | 合并 Segment、清理删除数据 | 占用 IO/CPU，可能影响前台负载 |

## 完整代码

基础代码见 `../demos/basic-search`，生产观察建议配合 `docker compose logs -f standalone` 和第 20 章监控指标阅读。

## 常见错误

| 现象 | 可能组件 | 排查方向 |
|---|---|---|
| insert 返回慢 | Proxy/Streaming Node/WAL | 看写入吞吐、WAL 延迟、批大小 |
| search 慢 | QueryNode/Proxy | 看 Collection load 状态、Segment 数量、索引参数 |
| create index 慢 | DataCoord/IndexNode | 看索引任务队列、CPU/GPU、对象存储吞吐 |
| 元数据异常 | RootCoord/etcd | 检查 etcd 健康和磁盘空间 |

## 面试题

1. Milvus 为什么要把 Coord 和 Node 拆开？
2. 写入成功和可被索引搜索之间为什么可能有时间差？
3. Segment 过碎会带来什么问题？
4. etcd 和对象存储分别保存什么？
5. Standalone 与 Cluster 的主要差异是什么？

## 练习题

1. 启动 Milvus 后插入 10 万条随机向量，观察日志中的 Segment 和 Flush 信息。
2. 在搜索前后分别调用 `load_collection` 和 `release_collection`，比较延迟和错误信息。
3. 故意频繁 flush，观察搜索性能和 Segment 数量变化。

## 小结

理解 Milvus 架构的关键是抓住两条链路：写入链路把数据可靠地变成 Segment 和索引，查询链路把分散在多个 QueryNode 的局部结果归并成全局 TopK。后续所有调优都离不开这两条链路。
