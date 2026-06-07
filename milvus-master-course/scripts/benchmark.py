from __future__ import annotations

import runpy
from pathlib import Path

if __name__ == "__main__":
    benchmark = Path(__file__).resolve().parents[1] / "demos" / "benchmark" / "benchmark.py"
    runpy.run_path(str(benchmark), run_name="__main__")
