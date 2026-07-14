import logging
from typing import Any, Dict, List, Optional
import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from app.core.config import settings

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.is_configured = self.api_key and self.api_key != "dummy_gemini_api_key"
        
        # Initialize Qdrant Client (gracefully falls back if connection fails)
        try:
            self.qdrant_client = QdrantClient(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT,
                api_key=settings.QDRANT_API_KEY
            )
            # Create collection if not exists (768 dimensions for Gemini text-embedding-004)
            self._init_qdrant_collections()
        except Exception as e:
            logger.warning(f"Failed to initialize Qdrant Client: {e}. Falling back to mock vector store.")
            self.qdrant_client = None
            self.mock_store = {}  # Fallback in-memory storage for local dev

    def _init_qdrant_collections(self):
        if not self.qdrant_client:
            return
        collections = ["resumes", "jobs"]
        for c in collections:
            try:
                # check if collection exists
                self.qdrant_client.get_collection(collection_name=c)
            except Exception:
                # create collection
                self.qdrant_client.create_collection(
                    collection_name=c,
                    vectors_config=VectorParams(size=768, distance=Distance.COSINE)
                )

    async def get_embedding(self, text: str) -> List[float]:
        """Generate text embeddings using Gemini embed_content model or fallback mock float vector."""
        if not self.is_configured:
            # Return dummy 768-dimension vector
            return [0.01] * 768
        try:
            import asyncio
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: genai.embed_content(
                    model="models/text-embedding-004",
                    contents=text,
                    task_type="retrieval_document"
                )
            )
            return response["embedding"]
        except Exception as e:
            logger.error(f"Failed to generate embedding from Gemini: {e}")
            return [0.01] * 768

    async def store_resume_vector(self, resume_id: str, text: str, metadata: Dict[str, Any]):
        """Store resume embedding vector in Qdrant or mock storage."""
        vector = await self.get_embedding(text)
        if self.qdrant_client:
            try:
                self.qdrant_client.upsert(
                    collection_name="resumes",
                    points=[
                        PointStruct(
                            id=resume_id,
                            vector=vector,
                            payload=metadata
                        )
                    ]
                )
                logger.info(f"Successfully upserted resume vector {resume_id} in Qdrant.")
            except Exception as e:
                logger.error(f"Qdrant upsert failed: {e}. Storing in mock memory.")
                self._store_mock(resume_id, vector, metadata)
        else:
            self._store_mock(resume_id, vector, metadata)

    def _store_mock(self, entity_id: str, vector: List[float], metadata: Dict[str, Any]):
        if not hasattr(self, 'mock_store'):
            self.mock_store = {}
        self.mock_store[entity_id] = {
            "vector": vector,
            "metadata": metadata
        }

    async def search_candidates(self, query_text: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search similar resume vector embeddings using semantic search."""
        query_vector = await self.get_embedding(query_text)
        results = []
        if self.qdrant_client:
            try:
                search_res = self.qdrant_client.search(
                    collection_name="resumes",
                    query_vector=query_vector,
                    limit=limit
                )
                for r in search_res:
                    results.append({
                        "resume_id": r.id,
                        "score": r.score,
                        "metadata": r.payload
                    })
                return results
            except Exception as e:
                logger.error(f"Qdrant search failed: {e}. Searching in mock memory.")
        
        # Fallback Mock Memory Search
        mock_data = getattr(self, 'mock_store', {})
        for rid, item in mock_data.items():
            results.append({
                "resume_id": rid,
                "score": 0.85,  # Dummy score
                "metadata": item["metadata"]
            })
        return results[:limit]
