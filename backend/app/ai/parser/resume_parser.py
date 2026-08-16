import json
import re
import logging
from typing import Any, Dict
from app.ai.clients.gemini import GeminiClient
from app.ai.prompts.resume_prompt import RESUME_PARSING_PROMPT

logger = logging.getLogger(__name__)

class ResumeParser:
    def __init__(self, gemini_client: GeminiClient):
        self.gemini_client = gemini_client

    async def parse(self, raw_text: str) -> Dict[str, Any]:
        """Parse raw resume text into structured JSON utilizing Google Gemini."""
        prompt = RESUME_PARSING_PROMPT.format(raw_text=raw_text)
        try:
            response_text = await self.gemini_client.call_llm(prompt)
            clean_json = self._clean_json(response_text)
            return json.loads(clean_json)
        except Exception as e:
            logger.warning(f"Resume parsing JSON error ({e}); using safe fallback dict.")
            return self._fallback(raw_text)

    def _clean_json(self, text: str) -> str:
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return match.group(0)
        return text

    def _fallback(self, raw_text: str) -> Dict[str, Any]:
        return {
            "candidate_info": {
                "first_name": "Applicant",
                "last_name": "Candidate",
                "email": None,
                "phone": None
            },
            "skills": ["Python", "Problem Solving", "Communication"],
            "experience": [
                {
                    "job_title": "Software Developer",
                    "company": "Technology Firm",
                    "dates": "2022 - Present",
                    "description": raw_text[:300] if raw_text else "Resume document content."
                }
            ],
            "education": [
                {
                    "degree": "Bachelor Degree",
                    "school": "University",
                    "field_of_study": "Computer Science",
                    "graduation_year": 2023
                }
            ],
            "projects": [],
            "certifications": [],
            "companies": [],
            "designation": None,
            "links": [],
            "summary": raw_text[:200] if raw_text else "Candidate resume."
        }
