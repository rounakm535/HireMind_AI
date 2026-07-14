import json
from typing import Any, Dict, List
from app.ai.clients.gemini import GeminiClient
from app.ai.prompts.ranking_prompt import CANDIDATE_RANKING_PROMPT

class CandidateRanker:
    def __init__(self, gemini_client: GeminiClient):
        self.gemini_client = gemini_client

    async def rank_candidates(self, job_description: str, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Rank multiple candidates based on skills, experience, and match metrics."""
        # Serialize list of candidates
        candidates_str = ""
        for c in candidates:
            candidates_str += f"- Candidate ID: {c.get('id')}, Name: {c.get('name')}, Match Score: {c.get('score')}, Summary: {c.get('summary')}\n"

        prompt = CANDIDATE_RANKING_PROMPT.format(
            job_description=job_description,
            candidates_list=candidates_str
        )
        response_text = await self.gemini_client.call_llm(prompt)
        clean_json = self._clean_json(response_text)
        return json.loads(clean_json)

    def _clean_json(self, text: str) -> str:
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
