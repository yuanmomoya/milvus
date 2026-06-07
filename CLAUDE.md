# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Chinese-language Milvus tutorial ("Milvus 从入门到精通") with 40 chapters of documentation, 7 runnable demo applications, and a companion HyperFrames video series. All Python code targets 3.11; all comments, docs, and narration are in Chinese.

The workspace root contains two parallel sub-projects:
- `milvus-master-course/` — tutorial code, docs, demos, and Docker Compose stack
- `milvus-master-course-vidoe/` — HyperFrames video scripts, narration, and TTS tooling (one directory per chapter)

Commands in this file assume the relevant sub-project is the working directory.

## Tech Stack

- Milvus 2.6.15 (standalone via Docker Compose)
- pymilvus 2.6.12 (`MilvusClient` API only — never use the legacy ORM `Collection` class)
- sentence-transformers (BAAI/bge-small-zh-v1.5, dim=384)
- CLIP (transformers + torch for image/multimodal demos)
- FastAPI + uvicorn for API services
- LangChain for RAG orchestration
- OpenAI-compatible API for LLM calls (works with Ollama/vLLM locally)
- HyperFrames (HTML-based) for the video series; 豆包 TTS for narration audio

## Commands

### Tutorial code (`milvus-master-course/`)

```bash
# Setup
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Start/stop Milvus (etcd + MinIO + standalone)
./scripts/start.sh
./scripts/stop.sh

# Health check
curl http://localhost:9091/healthz

# Initialize sample data (requires running Milvus)
python scripts/init_data.py

# Run a specific demo (each has its own .env.example)
cd demos/basic-search && cp .env.example .env && python main.py

# Run RAG API
cd demos/rag-system && cp .env.example .env && uvicorn main:app --reload --port 8001

# Run benchmark
cd demos/benchmark && python benchmark.py --rows 10000 --dim 384 --index HNSW --concurrency 4
```

### Video series (`milvus-master-course-vidoe/`)

The pipeline is `narration.txt → TTS → narration_timing.json → index.html → chapter-XX.mp4`. See `VIDEO_GUIDE.md` for the full design system, scene timing rules, subtitle spec, and 豆包 TTS API reference.

```bash
# 1. Edit chapter-XX/narration.txt (paragraphs separated by blank lines, one per scene)

# 2. Batch-generate TTS audio + per-scene timing JSON for ALL chapters
python3 build_narration.py
# Or single-shot synthesis:
python3 doubao_tts.py "要合成的文本" -o chapter-XX/narration.mp3

# 3. Generate index.html for ALL chapters (subtitle layer, GSAP timeline aligned to timing.json)
python3 gen_all_chapters.py

# 4. Render. HyperFrames REQUIRES Node 22 — load nvm before invoking
source ~/.nvm/nvm.sh && nvm use 22
cd chapter-01-vector-database-basics
npx hyperframes render --output chapter-01.mp4

# Or render all chapters (skips ones with existing mp4):
bash render_all.sh
```

Per-chapter artifacts: `narration.txt` (source), `narration.mp3` (TTS output), `narration_timing.json` (per-scene start/duration, drives HTML), `index.html` (HyperFrames composition), `chapter-XX.mp4` (final render). Track overall status in `PROGRESS.md`.

## Architecture Patterns

- All demos use `MilvusClient` (the newer high-level API), not the legacy ORM.
- Configuration via environment variables + `.env` files (python-dotenv). Each demo has `.env.example`.
- Embedding models are loaded once at startup and reused across requests.
- Vector writes use `upsert` for idempotency. Primary keys are content-hash based (SHA1) in the RAG system.
- HNSW with COSINE metric is the default index; IVF_FLAT used only in benchmark comparisons.
- RAG pipeline (demos/rag-system): `config.py` (Settings) → `embeddings.py` (encode) → `vector_store.py` (Milvus CRUD) → `main.py` (FastAPI routes with chunking, rewrite, rerank, LLM generation).
- Hybrid search uses multiple vector fields (title + body) with `RRFRanker` fusion.
- Each video chapter is a self-contained HyperFrames composition: `index.html` (scenes + GSAP timeline) paired with `narration.md` (per-scene text), `narration.mp3` (TTS output), and the rendered `chapter-XX.mp4`. Global look-and-feel (palette, typography, motion) lives in `milvus-master-course-vidoe/design.md`; chapter HTML must stay consistent with it.

## Conventions

- `from __future__ import annotations` in every Python file.
- Frozen dataclasses for configuration objects (never Pydantic Settings for config — Pydantic is only for API request/response models).
- Logging via stdlib `logging` (not print for operational messages).
- Chinese docstrings, comments, narration, and doc prose throughout. Mermaid diagrams for architecture/flow visualization.
- Video scenes target 8-12 seconds each, total chapter 90-120 seconds; animation timings in `index.html` must align with the matching `narration.md` segment.

## Environment Variables

Key variables (see `.env.example` in each demo):
- `MILVUS_URI` — Milvus endpoint (default: `http://localhost:19530`)
- `MILVUS_TOKEN` — auth token (empty for local dev)
- `EMBEDDING_MODEL` — HuggingFace model name (default: `BAAI/bge-small-zh-v1.5`)
- `OPENAI_BASE_URL` / `OPENAI_API_KEY` / `OPENAI_MODEL` — LLM for RAG answers
- `RECREATE_COLLECTION` — set to `true` to drop and recreate on startup (useful during dev)

## Docker Services

| Service | Port | Purpose |
|---------|------|---------|
| Milvus standalone | 19530 (gRPC), 9091 (health) | Vector database |
| MinIO | 9000 (API), 9001 (console) | Object storage for segments |
| etcd | 2379 (internal only) | Metadata coordination |
