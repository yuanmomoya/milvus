# benchmark

Milvus 插入与搜索压测 Demo。

```bash
cd milvus-master-course
./scripts/start.sh
cd demos/benchmark
cp .env.example .env
python benchmark.py --rows 10000 --dim 384 --index HNSW --concurrency 4
python benchmark.py --rows 10000 --dim 384 --index IVF_FLAT --concurrency 4
```
