from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.rag_engine import RAGEngine

app = FastAPI(
    title="AI-Powered RAG System & Contextual Search API",
    description="Engineered Retrieval-Augmented Generation (RAG) platform using Vector Embeddings & FAISS",
    version="1.0.0"
)

# Initialize RAG Engine Instance
rag_pipeline = RAGEngine()

class DocumentIngestRequest(BaseModel):
    document_text: str = Field(..., example="AWS Lambda is a serverless compute service that runs code in response to events.")

class QueryRequest(BaseModel):
    question: str = Field(..., example="What is AWS Lambda?")
    top_k: int = Field(default=2, ge=1, le=5)

@app.get("/health")
def health_check():
    return {"status": "UP", "indexed_chunks": len(rag_pipeline.documents)}

@app.post("/ingest")
def ingest_document(payload: DocumentIngestRequest):
    if not payload.document_text.strip():
        raise HTTPException(status_code=400, detail="Document text cannot be empty.")
    
    chunks_added = rag_pipeline.ingest_document(payload.document_text)
    return {
        "status": "success",
        "message": f"Successfully ingested and indexed {chunks_added} chunks.",
        "total_documents_indexed": len(rag_pipeline.documents)
    }

@app.post("/query")
def query_rag(payload: QueryRequest):
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    result = rag_pipeline.generate_rag_response(payload.question, payload.top_k)
    return result
