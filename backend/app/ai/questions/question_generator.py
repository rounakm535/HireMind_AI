import json
from typing import Any, Dict
from app.ai.clients.gemini import GeminiClient
from app.ai.prompts.questions_prompt import INTERVIEW_QUESTION_PROMPT

class QuestionGenerator:
    def __init__(self, gemini_client: GeminiClient):
        self.gemini_client = gemini_client

    async def generate_questions(self, job_description: str, resume_text: str, skill_gaps: Dict[str, Any]) -> Dict[str, Any]:
        """Generate targeted interview questions based on job description, resume, and skill gaps."""
        prompt = INTERVIEW_QUESTION_PROMPT.format(
            job_description=job_description,
            resume_text=resume_text,
            skill_gaps=json.dumps(skill_gaps)
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
