import json
from typing import Any, Dict
from app.ai.clients.gemini import GeminiClient
from app.ai.prompts.resume_prompt import RESUME_PARSING_PROMPT

class ResumeParser:
    def __init__(self, gemini_client: GeminiClient):
        self.gemini_client = gemini_client

    async def parse(self, raw_text: str) -> Dict[str, Any]:
        """Parse raw resume text into structured JSON utilizing Google Gemini."""
        prompt = RESUME_PARSING_PROMPT.format(raw_text=raw_text)
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
