import json
from typing import Any, Dict, List, Optional
import google.generativeai as genai
from app.core.config import settings
from app.ai import prompts
from app.exceptions.custom import AIServiceError
from app.schemas.resume import ResumeParsingResult, ResumeMatchResult


class GeminiClient:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.is_configured = self.api_key and self.api_key != "dummy_gemini_api_key"
        if self.is_configured:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-1.5-pro")
        else:
            self.model = None

    async def _call_llm(self, prompt: str) -> str:
        """Helper to invoke Gemini with exception handling and fallback."""
        if not self.is_configured:
            # Fallback mock responses when API key is not set
            return self._get_mock_response(prompt)

        try:
            # Run in executor if necessary, google sdk is synchronous
            import asyncio
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, lambda: self.model.generate_content(prompt)
            )
            return response.text
        except Exception as e:
            raise AIServiceError(f"Gemini API call failed: {str(e)}")

    def _get_mock_response(self, prompt: str) -> str:
        """Generates realistic mock data for local testing when no Gemini key is provided."""
        if "RESUME_PARSING_PROMPT" in prompt or "Parser" in prompt:
            return json.dumps({
                "candidate_info": {
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john.doe@example.com",
                    "phone": "+1-555-0199"
                },
                "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "Git"],
                "experience": [
                    {
                        "job_title": "Software Engineer",
                        "company": "Tech Corp",
                        "dates": "2022 - Present",
                        "description": "Built REST APIs with Python and FastAPI."
                    }
                ],
                "education": [
                    {
                        "degree": "Bachelor of Science in Computer Science",
                        "school": "State University",
                        "field_of_study": "Computer Science",
                        "graduation_year": 2022
                    }
                ],
                "summary": "Experienced Python Developer specializing in API backend engineering."
            })
        elif "RESUME_MATCHING_PROMPT" in prompt or "Recruiter" in prompt:
            return json.dumps({
                "score": 85.5,
                "fit_explanation": "The candidate has strong Python and FastAPI experience matching core backend requirements, but lacks AWS experience specified as preferred."
            })
        elif "SKILL_GAP_PROMPT" in prompt or "skills list" in prompt:
            return json.dumps({
                "matched_skills": ["Python", "FastAPI", "PostgreSQL"],
                "missing_skills": ["AWS S3", "Redis"],
                "additional_skills": ["Docker", "Git"]
            })
        elif "INTERVIEW_QUESTION_PROMPT" in prompt or "interview questions" in prompt:
            return json.dumps({
                "questions": [
                    {
                        "question": "Can you explain how concurrency works in FastAPI using async/await?",
                        "expected_answer": "Explain asyncio event loop, thread pool offloading for sync routes, and cooperative multitasking.",
                        "category": "Technical"
                    },
                    {
                        "question": "Describe a scenario where you had to debug a slow database query in PostgreSQL.",
                        "expected_answer": "Use of EXPLAIN ANALYZE, indexing, optimizing joins, or query rewriting.",
                        "category": "Technical"
                    }
                ]
            })
        elif "CANDIDATE_RANKING_PROMPT" in prompt or "Rank" in prompt:
            return json.dumps({
                "rankings": [],
                "reasoning": "Mock rank explanation."
            })
        elif "SUMMARY_GENERATOR_PROMPT" in prompt or "profile summary" in prompt:
            return "Highly skilled backend engineer with hands-on experience in building scalable REST APIs and microservices using Python."
        return "{}"

    async def parse_resume(self, raw_text: str) -> ResumeParsingResult:
        prompt = prompts.RESUME_PARSING_PROMPT.format(raw_text=raw_text)
        response_text = await self._call_llm(prompt)
        # Clean response if LLM returned markdown code blocks
        clean_text = self._clean_json_response(response_text)
        data = json.loads(clean_text)
        return ResumeParsingResult(**data)

    async def match_resume(
        self, resume_text: str, job_title: str, job_requirements: str, job_description: str
    ) -> ResumeMatchResult:
        prompt = prompts.RESUME_MATCHING_PROMPT.format(
            resume_text=resume_text,
            job_title=job_title,
            job_requirements=job_requirements,
            job_description=job_description,
        )
        response_text = await self._call_llm(prompt)
        clean_text = self._clean_json_response(response_text)
        data = json.loads(clean_text)
        
        # Skill gap analysis run as part of matching pipeline
        gap_prompt = prompts.SKILL_GAP_PROMPT.format(
            job_requirements=job_requirements,
            candidate_skills=resume_text[:2000] # Pass snippet of skills
        )
        gap_response = await self._call_llm(gap_prompt)
        gap_data = json.loads(self._clean_json_response(gap_response))

        # Questions run
        q_prompt = prompts.INTERVIEW_QUESTION_PROMPT.format(
            job_description=job_description,
            resume_text=resume_text,
            skill_gaps=json.dumps(gap_data)
        )
        q_response = await self._call_llm(q_prompt)
        q_data = json.loads(self._clean_json_response(q_response))

        return ResumeMatchResult(
            score=data.get("score", 0.0),
            fit_explanation=data.get("fit_explanation", ""),
            skill_gap=gap_data,
            suggested_questions=q_data.get("questions", [])
        )

    async def generate_email(self, template_type: str, candidate_name: str, job_title: str, recruiter_name: str) -> Dict[str, str]:
        prompt = f"""
        Write a professional {template_type} email from recruiter {recruiter_name} to candidate {candidate_name} for the position of {job_title}.
        Return a JSON response with keys: 'subject' and 'body'. Do not include markdown code block syntax.
        """
        response_text = await self._call_llm(prompt)
        clean_text = self._clean_json_response(response_text)
        try:
            return json.loads(clean_text)
        except Exception:
            return {
                "subject": f"Update regarding your application for {job_title}",
                "body": f"Hello {candidate_name},\n\nWe are writing to update you on your application for the {job_title} role.\n\nBest regards,\n{recruiter_name}"
            }

    async def chat_interaction(self, query: str, context: str) -> str:
        prompt = f"""
        You are HireMind AI Assistant. Help the recruiter answer their query using the context below.
        Context:
        {context}

        Recruiter Query:
        {query}
        """
        return await self._call_llm(prompt)

    def _clean_json_response(self, text: str) -> str:
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
