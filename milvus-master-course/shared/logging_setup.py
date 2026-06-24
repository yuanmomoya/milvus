"""共享日志配置

统一日志格式和级别，避免每个 Demo 重复配置。
"""
from __future__ import annotations

import logging
import os

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s - %(message)s"


def configure_logging(name: str) -> logging.Logger:
    """配置日志并返回指定名称的 Logger 实例"""
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format=LOG_FORMAT,
    )
    return logging.getLogger(name)
