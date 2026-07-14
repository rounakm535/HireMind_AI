import logging
from typing import Any, Dict, List
from app.ai.clients.gemini import GeminiClient
from app.ai.embeddings.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)

class RecruiterChat:
    def __init__(self, gemini_client: GeminiClient, embedding_service: EmbeddingService):
        self.gemini_client = gemini_client
        self.embedding_service = embedding_service

    async def answer_query(self, query: str, organization_id: str) -> str:
        """Process natural language recruiter query using Qdrant vector semantic search + Gemini RAG."""
        logger.info(f"Processing recruiter query: {query}")
        
        # 1. Retrieve candidates semantic results from Qdrant
        search_results = await self.embedding_service.search_candidates(query, limit=5)
        
        # 2. Compile context string for RAG
        context_lines = []
        for index, r in enumerate(search_results):
            meta = r.get("metadata", {})
            # Ensure candidate belongs to this organization
            if meta.get("organization_id") == str(organization_id):
                context_lines.append(
                    f"{index + 1}. Candidate Name: {meta.get('first_name')} {meta.get('last_name')}, "
                    f"Email: {meta.get('email')}, Skills: {', '.join(meta.get('skills', []))}"
                )
        
        context_str = "\n".join(context_lines) if context_lines else "No similar candidates found in Qdrant vector store."

        # 3. Invoke Gemini
        prompt = f"""
        You are HireMind AI Assistant, an elite recruitment copilot.
        Answer the recruiter's query using the semantically retrieved candidate matches from the database context.

        Retrieved Candidates Context:
        {context_str}

        Recruiter Query:
        {query}

        If no candidates are in the context, guide the recruiter on how to upload resumes to begin matching.
        Return a warm, recruiter-friendly Markdown response.
        """
        return await self.gemini_client.call_llm(prompt)
