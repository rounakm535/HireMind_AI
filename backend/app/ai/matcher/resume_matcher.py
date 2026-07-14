import json
from typing import Any, Dict
from app.ai.clients.gemini import GeminiClient
from app.ai.prompts.match_prompt import RESUME_MATCHING_PROMPT, SKILL_GAP_PROMPT

class ResumeMatcher:
    def __init__(self, gemini_client: GeminiClient):
        self.gemini_client = gemini_client

    async def match(self, resume_text: str, job_title: str, job_description: str, job_requirements: str) -> Dict[str, Any]:
        """Perform semantic resume matching against job postings."""
        prompt = RESUME_MATCHING_PROMPT.format(
            resume_text=resume_text,
            job_title=job_title,
            job_description=job_description,
            job_requirements=job_requirements
        )
        response_text = await self.gemini_client.call_llm(prompt)
        clean_json = self._clean_json(response_text)
        return json.loads(clean_json)

    async def analyze_skill_gap(self, candidate_skills: str, job_requirements: str) -> Dict[str, Any]:
        """Perform dedicated skill gap analysis comparison."""
        prompt = SKILL_GAP_PROMPT.format(
            candidate_skills=candidate_skills,
            job_requirements=job_requirements
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
