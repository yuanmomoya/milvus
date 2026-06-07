"""RAG 知识库问答系统 - PDF 导入脚本

解析 PDF 文件并通过 FastAPI 接口导入到 RAG 知识库。
用法: python ingest_pdf.py <pdf_path>
"""
from __future__ import annotations

import argparse
from pathlib import Path

from pypdf import PdfReader
from fastapi.testclient import TestClient

from main import app


def read_pdf(path: Path) -> str:
    """解析 PDF 文件，提取所有页面的文本内容

    每页文本前添加页码标记，方便后续追溯来源。
    """
    reader = PdfReader(str(path))
    pages: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append(f"\n\n[page={index}]\n{text}")
    return "".join(pages)


def main() -> None:
    parser = argparse.ArgumentParser(description="导入 PDF 到 RAG 知识库")
    parser.add_argument("pdf", type=Path, help="PDF 文件路径")
    args = parser.parse_args()

    if not args.pdf.exists():
        print(f"文件不存在: {args.pdf}")
        return

    # 读取 PDF 文本
    text = read_pdf(args.pdf)
    if not text.strip():
        print("PDF 无有效文本内容")
        return

    # 通过 FastAPI TestClient 调用入库接口
    # 这样可以复用 main.py 中的切块和 Embedding 逻辑
    client = TestClient(app)
    response = client.post("/ingest/text", json={"source": args.pdf.name, "text": text})
    response.raise_for_status()
    result = response.json()
    print(f"导入完成: {args.pdf.name} → {result.get('chunks', 0)} 个切块")


if __name__ == "__main__":
    main()
