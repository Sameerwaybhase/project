# AI-Powered RAG System & Contextual Search

Retrieval-Augmented Generation (RAG) platform using **Python, FastAPI, SentenceTransformers, FAISS Vector Index, and REST APIs**.

## Features
1. **Document Ingestion**: Chunks raw text into semantic segments.
2. **Vector Embeddings**: Encodes text chunks into dense 384-dimensional vector space using HuggingFace models.
3. **FAISS Vector Store**: Fast L2 similarity search for relevant context retrieval.
4. **Contextual RAG Synthesis**: Generates augmented prompts grounding LLM responses in real document context.
5. **FastAPI REST Endpoints**: Asynchronous endpoints `/ingest`, `/query`, and `/health`.

## Repository Layout
* `app/main.py`: FastAPI server exposing RAG REST endpoints.
* `app/rag_engine.py`: Vector embedding, FAISS indexing, and context retrieval pipeline.
* `requirements.txt`: Project dependencies.
* `Dockerfile`: Container configuration for production deployment.
* `tests/test_rag.py`: Pytest automated unit tests.
