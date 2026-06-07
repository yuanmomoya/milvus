# 18 Milvus 集群部署

## 学习目标

学完本章后，你应该能够：

- 理解 Milvus 分布式集群的组件拓扑。
- 使用 Docker Compose 或 Helm 部署集群模式。
- 配置多 QueryNode、多 DataNode 实现水平扩展。
- 规划集群的资源分配和容量。
- 处理集群部署中的常见问题。

---

## Standalone vs Cluster

| 维度 | Standalone | Cluster |
|---|---|---|
| 组件 | 所有角色在一个进程 | Coord、Node 独立部署 |
| 扩展性 | 垂直扩展（加 CPU/内存） | 水平扩展（加节点） |
| 高可用 | 单点故障 | 组件级容错 |
| 适用规模 | < 2000 万向量 | > 2000 万或高可用要求 |
| 运维复杂度 | 低 | 高 |
| 依赖 | etcd + MinIO | etcd + MinIO/S3 + Pulsar/Kafka |

---

## 集群架构

```mermaid
flowchart TB
    Client[SDK / 应用] --> LB[负载均衡]
    LB --> Proxy1[Proxy 1]
    LB --> Proxy2[Proxy 2]

    Proxy1 --> RC[RootCoord]
    Proxy1 --> DC[DataCoord]
    Proxy1 --> QC[QueryCoord]
    Proxy1 --> IC[IndexCoord]
    Proxy2 --> RC
    Proxy2 --> DC
    Proxy2 --> QC
    Proxy2 --> IC

    DC --> DN1[DataNode 1]
    DC --> DN2[DataNode 2]
    QC --> QN1[QueryNode 1]
    QC --> QN2[QueryNode 2]
    QC --> QN3[QueryNode 3]
    IC --> IN1[IndexNode 1]
    IC --> IN2[IndexNode 2]

    subgraph 基础设施
        Etcd[(etcd 集群)]
        MQ[(Pulsar / Kafka)]
        S3[(S3 / MinIO)]
    end

    RC --> Etcd
    DC --> Etcd
    DN1 --> MQ
    DN2 --> MQ
    QN1 --> S3
    IN1 --> S3
```

### 组件角色

| 组件 | 可扩展 | 职责 | 扩展场景 |
|---|---|---|---|
| Proxy | 是 | 接入请求、路由 | QPS 高时加 Proxy |
| RootCoord | 否（单实例） | DDL、时间戳 | 无需扩展 |
| DataCoord | 否（单实例） | Segment 调度 | 无需扩展 |
| QueryCoord | 否（单实例） | 查询调度 | 无需扩展 |
| IndexCoord | 否（单实例） | 索引任务调度 | 无需扩展 |
| DataNode | 是 | 写入消费 | 写入吞吐不足时加 |
| QueryNode | 是 | 搜索执行 | 搜索延迟高/QPS 不足时加 |
| IndexNode | 是 | 索引构建 | 索引构建慢时加 |

---

## Docker Compose 集群部署

适合开发测试和小规模生产：

```yaml
name: milvus-cluster

services:
  etcd:
    image: quay.io/coreos/etcd:v3.5.18
    command: >
      etcd
      -advertise-client-urls=http://127.0.0.1:2379
      -listen-client-urls=http://0.0.0.0:2379
      --data-dir=/etcd
    volumes:
      - etcd-data:/etcd
    healthcheck:
      test: ['CMD', 'etcdctl', 'endpoint', 'health']
      interval: 30s
      timeout: 20s
      retries: 3

  minio:
    image: minio/minio:RELEASE.2024-12-18T13-15-44Z
    environment:
      MINIO_ACCESS_KEY: minioadmin
      MINIO_SECRET_KEY: minioadmin
    command: minio server /minio_data --console-address ':9001'
    ports:
      - '9000:9000'
      - '9001:9001'
    volumes:
      - minio-data:/minio_data
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:9000/minio/health/live']
      interval: 30s
      timeout: 20s
      retries: 3

  pulsar:
    image: apachepulsar/pulsar:3.1.2
    command: bin/pulsar standalone
    ports:
      - '6650:6650'
    volumes:
      - pulsar-data:/pulsar/data
    healthcheck:
      test: ['CMD', 'bin/pulsar-admin', 'brokers', 'healthcheck']
      interval: 30s
      timeout: 20s
      retries: 3

  rootcoord:
    image: milvusdb/milvus:v2.6.15
    command: ['milvus', 'run', 'rootcoord']
    environment: &milvus-env
      ETCD_ENDPOINTS: etcd:2379
      MINIO_ADDRESS: minio:9000
      PULSAR_ADDRESS: pulsar://pulsar:6650
      MINIO_ACCESS_KEY: minioadmin
      MINIO_SECRET_KEY: minioadmin
    depends_on:
      etcd: { condition: service_healthy }
      minio: { condition: service_healthy }
      pulsar: { condition: service_healthy }

  datacoord:
    image: milvusdb/milvus:v2.6.15
    command: ['milvus', 'run', 'datacoord']
    environment: *milvus-env
    depends_on:
      etcd: { condition: service_healthy }
      minio: { condition: service_healthy }
      pulsar: { condition: service_healthy }

  querycoord:
    image: milvusdb/milvus:v2.6.15
    command: ['milvus', 'run', 'querycoord']
    environment: *milvus-env
    depends_on:
      etcd: { condition: service_healthy }
      minio: { condition: service_healthy }
      pulsar: { condition: service_healthy }

  indexcoord:
    image: milvusdb/milvus:v2.6.15
    command: ['milvus', 'run', 'indexcoord']
    environment: *milvus-env
    depends_on:
      etcd: { condition: service_healthy }
      minio: { condition: service_healthy }
      pulsar: { condition: service_healthy }

  datanode:
    image: milvusdb/milvus:v2.6.15
    command: ['milvus', 'run', 'datanode']
    environment: *milvus-env
    depends_on:
      etcd: { condition: service_healthy }
      minio: { condition: service_healthy }
      pulsar: { condition: service_healthy }

  querynode1:
    image: milvusdb/milvus:v2.6.15
    command: ['milvus', 'run', 'querynode']
    environment: *milvus-env
    depends_on:
      etcd: { condition: service_healthy }
      minio: { condition: service_healthy }
      pulsar: { condition: service_healthy }

  querynode2:
    image: milvusdb/milvus:v2.6.15
    command: ['milvus', 'run', 'querynode']
    environment: *milvus-env
    depends_on:
      etcd: { condition: service_healthy }
      minio: { condition: service_healthy }
      pulsar: { condition: service_healthy }

  indexnode:
    image: milvusdb/milvus:v2.6.15
    command: ['milvus', 'run', 'indexnode']
    environment: *milvus-env
    depends_on:
      etcd: { condition: service_healthy }
      minio: { condition: service_healthy }
      pulsar: { condition: service_healthy }

  proxy:
    image: milvusdb/milvus:v2.6.15
    command: ['milvus', 'run', 'proxy']
    environment: *milvus-env
    ports:
      - '19530:19530'
      - '9091:9091'
    depends_on:
      rootcoord: { condition: service_started }
      datacoord: { condition: service_started }
      querycoord: { condition: service_started }
      indexcoord: { condition: service_started }

volumes:
  etcd-data:
  minio-data:
  pulsar-data:
```

---

## Helm 部署（Kubernetes）

生产环境推荐使用 Helm Chart 部署到 Kubernetes：

```bash
# 添加 Milvus Helm 仓库
helm repo add milvus https://zilliztech.github.io/milvus-helm/
helm repo update

# 安装集群模式
helm install milvus milvus/milvus \
  --set cluster.enabled=true \
  --set queryNode.replicas=3 \
  --set dataNode.replicas=2 \
  --set indexNode.replicas=2 \
  --set proxy.replicas=2 \
  -n milvus --create-namespace
```

### 自定义 values.yaml

```yaml
cluster:
  enabled: true

queryNode:
  replicas: 3
  resources:
    requests:
      memory: "8Gi"
      cpu: "4"
    limits:
      memory: "16Gi"
      cpu: "8"

dataNode:
  replicas: 2
  resources:
    requests:
      memory: "4Gi"
      cpu: "2"

indexNode:
  replicas: 2
  resources:
    requests:
      memory: "8Gi"
      cpu: "4"

proxy:
  replicas: 2
  resources:
    requests:
      memory: "2Gi"
      cpu: "2"

etcd:
  replicaCount: 3
  persistence:
    size: 10Gi

minio:
  mode: distributed
  replicas: 4
  persistence:
    size: 100Gi

pulsar:
  enabled: true
  # 或使用 Kafka
  # kafka:
  #   enabled: true
```

---

## 资源规划

### QueryNode 内存规划

QueryNode 需要加载索引和向量到内存：

```
单个 QueryNode 内存 ≈ 总数据内存 / QueryNode 数量 × 副本数

示例：
- 1000 万条 × 768 维 × HNSW(M=16) ≈ 31 GB
- 3 个 QueryNode，1 副本：每个 ~10.3 GB
- 3 个 QueryNode，2 副本：每个 ~20.6 GB
```

### 各组件资源建议

| 组件 | CPU | 内存 | 磁盘 | 数量 |
|---|---|---|---|---|
| Proxy | 2-4 核 | 2-4 GB | 无 | 2+（按 QPS） |
| QueryNode | 4-8 核 | 8-32 GB | SSD（mmap 时） | 按数据量 |
| DataNode | 2-4 核 | 4-8 GB | 无 | 2+（按写入量） |
| IndexNode | 4-8 核 | 8-16 GB | SSD（临时） | 1-2 |
| Coord 系列 | 1-2 核 | 2-4 GB | 无 | 各 1 |
| etcd | 2 核 | 4 GB | SSD 10-50 GB | 3（高可用） |
| Pulsar/Kafka | 4 核 | 8 GB | SSD 50-200 GB | 3+ |
| MinIO/S3 | 2 核 | 4 GB | HDD/SSD | 4+（分布式） |

---

## 扩缩容

### 水平扩展 QueryNode

当搜索延迟增加或 QPS 不足时：

```bash
# Helm 扩容
helm upgrade milvus milvus/milvus --set queryNode.replicas=5 -n milvus

# Docker Compose 扩容（添加新的 querynode 服务）
docker compose up -d --scale querynode=4
```

QueryCoord 会自动将 Segment 重新分配到新的 QueryNode。

### 扩展 DataNode

当写入吞吐不足时：

```bash
helm upgrade milvus milvus/milvus --set dataNode.replicas=4 -n milvus
```

### 扩展 IndexNode

当索引构建积压时：

```bash
helm upgrade milvus milvus/milvus --set indexNode.replicas=4 -n milvus
```

---

## 消息队列选择

| 消息队列 | 优点 | 缺点 | 适用场景 |
|---|---|---|---|
| Pulsar | Milvus 默认支持，功能完整 | 部署复杂，资源占用大 | 生产集群 |
| Kafka | 生态成熟，运维经验多 | 需要额外配置 | 已有 Kafka 集群 |
| RocksMQ | 内嵌，无需额外部署 | 不支持集群模式 | 仅 Standalone |

---

## 集群健康检查

```bash
# 检查所有组件状态
kubectl get pods -n milvus

# 检查 Milvus 健康
curl http://<proxy-ip>:9091/healthz

# 查看组件日志
kubectl logs -f deployment/milvus-proxy -n milvus
kubectl logs -f deployment/milvus-querynode -n milvus

# 查看 QueryNode 负载分布
# 通过 Prometheus 指标观察各 QueryNode 的 Segment 数量和内存使用
```

---

## 常见错误

| 现象 | 原因 | 修复 |
|---|---|---|
| Proxy 启动失败 | Coord 组件未就绪 | 检查 Coord 日志，确认 etcd 连接 |
| QueryNode OOM | 数据量超过单节点内存 | 增加 QueryNode 数量或开启 mmap |
| 写入延迟高 | Pulsar 积压 | 检查 Pulsar 健康，增加 DataNode |
| 索引构建慢 | IndexNode 资源不足 | 增加 IndexNode 或增大 CPU |
| etcd 空间不足 | 元数据过多 | 执行 etcd compaction，增大 quota |
| 搜索结果不一致 | Segment 正在迁移 | 等待 QueryCoord 完成 balance |

---

## 面试题

1. **Standalone 和 Cluster 的核心区别是什么？**
   Standalone 所有角色在一个进程，共享内存，用 RocksMQ 做消息队列。Cluster 各角色独立部署，通过 Pulsar/Kafka 通信，可以独立扩缩容。

2. **为什么 Coord 组件不需要多副本？**
   Coord 是调度器，不处理数据面流量。它的负载很轻，单实例足够。高可用通过 etcd 选主实现——Coord 挂了会自动重新选主恢复。

3. **增加 QueryNode 后搜索性能一定会提升吗？**
   不一定。如果瓶颈在网络、Proxy 或索引参数，加 QueryNode 无效。只有当 QueryNode CPU/内存是瓶颈时，水平扩展才有效。

4. **集群模式为什么需要 Pulsar/Kafka？**
   集群中 DataNode 和 QueryNode 是独立进程，需要通过消息队列传递写入日志。Standalone 用进程内的 RocksMQ 就够了。

5. **如何判断需要从 Standalone 升级到 Cluster？**
   当出现以下情况：单机内存不够加载所有数据、需要高可用（不能单点故障）、写入吞吐需要水平扩展、搜索 QPS 超过单机上限。

---

## 练习题

1. **Docker Compose 集群**：使用本章的 docker-compose 文件启动集群模式，验证写入和搜索正常工作。

2. **QueryNode 扩容**：启动 2 个 QueryNode 的集群，写入 10 万条数据。然后增加到 4 个 QueryNode，观察 Segment 重新分配过程。

3. **故障模拟**：停止一个 QueryNode（`docker stop`），观察搜索是否仍然正常（QueryCoord 应该将 Segment 迁移到其他节点）。

4. **资源监控**：使用 `docker stats` 观察集群各组件的 CPU 和内存使用，写入和搜索时分别观察哪个组件负载最高。

---

## 小结

Milvus 集群部署的核心是理解哪些组件可以水平扩展（Proxy、QueryNode、DataNode、IndexNode）以及何时需要扩展。QueryNode 决定搜索能力，DataNode 决定写入能力，IndexNode 决定索引构建速度。生产环境推荐 Helm + Kubernetes 部署，配合监控和自动扩缩容。
