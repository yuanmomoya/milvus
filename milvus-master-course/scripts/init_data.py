"""初始化样例数据脚本

委托 demos/basic-search/main.py 执行，避免重复代码。
等同于在 demos/basic-search/ 目录下运行 python main.py。
"""
from __future__ import annotations

import runpy
from pathlib import Path

if __name__ == "__main__":
    demo = Path(__file__).resolve().parents[1] / "demos" / "basic-search" / "main.py"
    runpy.run_path(str(demo), run_name="__main__")
