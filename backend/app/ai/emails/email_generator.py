import json
from typing import Any, Dict
from app.ai.clients.gemini import GeminiClient
from app.ai.prompts.email_prompt import EMAIL_GENERATOR_PROMPT

class EmailGenerator:
    def __init__(self, gemini_client: GeminiClient):
        self.gemini_client = gemini_client

    async def generate_email(
        self,
        template_type: str,
        candidate_name: str,
        job_title: str,
        recruiter_name: str,
        additional_context: str = ""
    ) -> Dict[str, str]:
        """Generate personalized emails from recruiters to candidates."""
        prompt = EMAIL_GENERATOR_PROMPT.format(
            template_type=template_type,
            candidate_name=candidate_name,
            job_title=job_title,
            recruiter_name=recruiter_name,
            additional_context=additional_context
        )
        response_text = await self.gemini_client.call_llm(prompt)
        clean_json = self._clean_json(response_text)
        try:
            return json.loads(clean_json)
        except Exception:
            return {
                "subject": f"Update regarding your application for {job_title}",
                "body": f"Hello {candidate_name},\n\nWe are writing to update you on your application for the {job_title} role.\n\nBest regards,\n{recruiter_name}"
            }

    def _clean_json(self, text: str) -> str:
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
