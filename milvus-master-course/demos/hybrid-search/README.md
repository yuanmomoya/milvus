# hybrid-search

演示 Milvus 多向量字段 Hybrid Search：标题向量和正文向量分别召回，再用 RRF 融合排序。

```bash
cd milvus-master-course
./scripts/start.sh
cd demos/hybrid-search
cp .env.example .env
python main.py
```
