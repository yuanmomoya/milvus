#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
docker compose up -d

printf '等待 Milvus 健康检查'
for _ in $(seq 1 60); do
  if curl -fsS http://localhost:9091/healthz >/dev/null 2>&1; then
    printf '
Milvus 已启动：http://localhost:19530
'
    exit 0
  fi
  printf '.'
  sleep 2
done

printf '
Milvus 启动超时，请执行 docker compose logs standalone 查看日志。
' >&2
exit 1
