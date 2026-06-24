"""main.py 核心函数单元测试：split_text / rewrite_query / rerank / build_prompt / call_llm。

由于 main.py 在模块级别初始化 EmbeddingService 和 RagVectorStore，
需在导入前 mock 掉 SentenceTransformer 和 MilvusClient 连接。
"""
from __future__ import annotations

import sys
from typing import Any
from unittest.mock import MagicMock, patch


def _import_rag_main():
    """延迟导入 main 模块，mock 掉重量级初始化。"""
    mock_model = MagicMock()
    mock_model.get_sentence_embedding_dimension.return_value = 384
    mock_model.encode.return_value = MagicMock(
        astype=MagicMock(return_value=MagicMock(tolist=MagicMock(return_value=[[0.0] * 384])))
    )

    mock_st = MagicMock()
    mock_st.SentenceTransformer.return_value = mock_model

    with patch.dict(sys.modules, {"sentence_transformers": mock_st}):
        with patch("pymilvus.MilvusClient"):
            if "main" in sys.modules:
                del sys.modules["main"]
            if "embeddings" in sys.modules:
                del sys.modules["embeddings"]
            import main as rag_main
            return rag_main


rag_main = _import_rag_main()
split_text = rag_main.split_text
rewrite_query = rag_main.rewrite_query
rerank = rag_main.rerank
build_prompt = rag_main.build_prompt
call_llm = rag_main.call_llm
Chunk = rag_main.Chunk


class TestSplitText:
    """split_text 应按配置大小切块并返回 Chunk 列表。"""

    def test_short_text_single_chunk(self) -> None:
        result = split_text("这是一段短文本。", source="test.md", chunk_size=600, chunk_overlap=100)
        assert len(result) == 1
        assert result[0].text == "这是一段短文本。"
        assert result[0].source == "test.md"
        assert result[0].chunk_id == 0

    def test_long_text_multiple_chunks(self) -> None:
        long_text = "这是一段内容。" * 200
        result = split_text(long_text, source="long.md", chunk_size=100, chunk_overlap=20)
        assert len(result) > 1
        for idx, chunk in enumerate(result):
            assert chunk.source == "long.md"
            assert chunk.chunk_id == idx

    def test_empty_text(self) -> None:
        result = split_text("", source="empty.md", chunk_size=600, chunk_overlap=100)
        assert result == []

    def test_chunk_ids_sequential(self) -> None:
        text = "第一段内容。\n\n第二段内容。\n\n第三段内容。" * 50
        result = split_text(text, source="seq.md", chunk_size=50, chunk_overlap=10)
        ids = [chunk.chunk_id for chunk in result]
        assert ids == list(range(len(result)))

    def test_returns_chunk_instances(self) -> None:
        result = split_text("向量数据库。", source="t.md", chunk_size=600, chunk_overlap=100)
        assert all(isinstance(c, Chunk) for c in result)


class TestRewriteQuery:
    """rewrite_query 应根据对话历史改写查询。"""

    def test_no_history_returns_original(self) -> None:
        assert rewrite_query("什么是向量数据库？", []) == "什么是向量数据库？"

    def test_with_history_includes_context(self) -> None:
        history = [{"role": "user", "content": "介绍一下 Milvus"}]
        result = rewrite_query("它支持什么？", history)
        assert "结合上下文" in result
        assert "介绍一下 Milvus" in result
        assert "它支持什么？" in result

    def test_uses_last_four_turns(self) -> None:
        history = [
            {"role": "user", "content": f"问题{i}"}
            for i in range(6)
        ]
        result = rewrite_query("最新问题", history)
        assert "问题2" in result
        assert "问题5" in result
        assert "问题0" not in result
        assert "问题1" not in result

    def test_missing_content_key(self) -> None:
        history = [{"role": "user"}, {"content": "有效内容"}]
        result = rewrite_query("问题", history)
        assert "有效内容" in result

    def test_empty_history_list(self) -> None:
        assert rewrite_query("查询", []) == "查询"


class TestRerank:
    """rerank 应基于字符重叠度对文档重排序。"""

    def _make_doc(self, text: str, score: float = 0.9) -> dict[str, Any]:
        return {"text": text, "score": score, "source": "test.md", "page": 0}

    def test_returns_top_n(self) -> None:
        docs = [self._make_doc(f"文档{i}") for i in range(10)]
        result = rerank("测试", docs, top_n=3)
        assert len(result) == 3

    def test_top_n_greater_than_docs(self) -> None:
        docs = [self._make_doc("文档")]
        result = rerank("测试", docs, top_n=5)
        assert len(result) == 1

    def test_adds_rerank_score(self) -> None:
        docs = [self._make_doc("向量数据库检索")]
        result = rerank("向量", docs, top_n=1)
        assert "rerank_score" in result[0]
        assert isinstance(result[0]["rerank_score"], float)

    def test_higher_overlap_ranked_first(self) -> None:
        docs = [
            self._make_doc("完全不相关的文本"),
            self._make_doc("向量数据库支持向量检索"),
        ]
        result = rerank("向量检索", docs, top_n=2)
        assert "向量" in result[0]["text"]

    def test_empty_docs(self) -> None:
        result = rerank("问题", [], top_n=5)
        assert result == []

    def test_empty_question(self) -> None:
        docs = [self._make_doc("内容")]
        result = rerank("", docs, top_n=1)
        assert len(result) == 1

    def test_preserves_original_fields(self) -> None:
        doc = {"text": "milvus", "score": 0.85, "source": "file.md", "page": 3, "chunk_id": 7}
        result = rerank("milvus", [doc], top_n=1)
        assert result[0]["source"] == "file.md"
        assert result[0]["page"] == 3
        assert result[0]["chunk_id"] == 7
        assert result[0]["score"] == 0.85


class TestBuildPrompt:
    """build_prompt 应组装带来源标注的 RAG Prompt。"""

    def test_includes_question(self) -> None:
        prompt = build_prompt("什么是 Milvus？", [])
        assert "什么是 Milvus？" in prompt

    def test_includes_docs_with_source_labels(self) -> None:
        docs = [
            {"text": "Milvus 是向量数据库", "source": "intro.md", "page": 1},
            {"text": "支持 HNSW 索引", "source": "index.md", "page": 5},
        ]
        prompt = build_prompt("介绍 Milvus", docs)
        assert "[来源 1]" in prompt
        assert "[来源 2]" in prompt
        assert "intro.md" in prompt
        assert "index.md" in prompt

    def test_system_instruction_present(self) -> None:
        prompt = build_prompt("问题", [])
        assert "知识库问答助手" in prompt
        assert "根据现有资料无法判断" in prompt

    def test_empty_docs(self) -> None:
        prompt = build_prompt("问题", [])
        assert "问题" in prompt


class TestCallLlm:
    """call_llm 在未配置 API Key 时应返回检索摘要。"""

    def test_no_key_returns_summary(self) -> None:
        result = call_llm("这是一段很长的 prompt 内容")
        assert "未配置 OPENAI_API_KEY" in result
        assert "prompt" in result
