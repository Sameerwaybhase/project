import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

class RAGEngine:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.dimension = 384
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents: List[str] = []

    def chunk_text(self, text: str, chunk_size: int = 300, overlap: int = 50) -> List[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks

    def ingest_document(self, text: str) -> int:
        chunks = self.chunk_text(text)
        if not chunks:
            return 0
        embeddings = self.model.encode(chunks)
        self.index.add(np.array(embeddings).astype('float32'))
        self.documents.extend(chunks)
        return len(chunks)

    def retrieve_context(self, question: str, top_k: int = 2) -> List[str]:
        if self.index.ntotal == 0:
            return []
        query_vector = self.model.encode([question]).astype('float32')
        distances, indices = self.index.search(query_vector, top_k)
        retrieved = [self.documents[idx] for idx in indices[0] if idx < len(self.documents)]
        return retrieved

    def generate_rag_response(self, question: str, top_k: int = 2) -> Dict[str, Any]:
        contexts = self.retrieve_context(question, top_k)
        context_str = "\n".join(contexts) if contexts else "No context available."
        
        augmented_prompt = (
            f"You are a helpful AI assistant. Answer the user's question using ONLY the context provided below.\n\n"
            f"--- Context ---\n{context_str}\n\n"
            f"--- Question ---\n{question}\n\n"
            f"--- Answer ---"
        )
        
        return {
            "question": question,
            "retrieved_contexts": contexts,
            "augmented_prompt": augmented_prompt,
            "synthesized_answer": f"Based on the provided context: {contexts[0]}" if contexts else "No relevant information found."
        }
