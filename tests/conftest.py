"""共享 pytest 夹具：统一 sys.path 设置与模块级 mock。"""
from __future__ import annotations

import sys
from pathlib import Path

# 各子项目目录加入 sys.path，保证 import 可达
_REPO = Path(__file__).resolve().parent.parent
_RAG_DIR = _REPO / "milvus-master-course" / "demos" / "rag-system"
_BENCH_DIR = _REPO / "milvus-master-course" / "demos" / "benchmark"
_VIDEO_DIR = _REPO / "milvus-master-course-vidoe"

for _p in (_RAG_DIR, _BENCH_DIR, _VIDEO_DIR):
    _s = str(_p)
    if _s not in sys.path:
        sys.path.insert(0, _s)
