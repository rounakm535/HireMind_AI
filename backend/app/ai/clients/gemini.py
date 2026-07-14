import json
import logging
from typing import Any, Dict, List, Optional
import google.generativeai as genai
from app.core.config import settings
from app.exceptions.custom import AIServiceError
from app.schemas.resume import ResumeParsingResult, ResumeMatchResult

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.is_configured = self.api_key and self.api_key != "dummy_gemini_api_key"
        if self.is_configured:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-1.5-pro")
        else:
            self.model = None

    async def call_llm(self, prompt: str) -> str:
        """Invoke the Google Gemini LLM model with fallback handling."""
        if not self.is_configured:
            logger.warning("Gemini API key not configured, using mock fallback.")
            return self._mock_response(prompt)
        try:
            import asyncio
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, lambda: self.model.generate_content(prompt)
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini LLM call exception: {e}")
            raise AIServiceError(f"Google Gemini LLM call failed: {str(e)}")

    async def parse_resume(self, raw_text: str) -> ResumeParsingResult:
        from app.ai.parser.resume_parser import ResumeParser
        parser = ResumeParser(self)
        data = await parser.parse(raw_text)
        return ResumeParsingResult(**data)

    async def match_resume(
        self, resume_text: str, job_title: str, job_requirements: str, job_description: str
    ) -> ResumeMatchResult:
        from app.ai.matcher.resume_matcher import ResumeMatcher
        from app.ai.questions.question_generator import QuestionGenerator
        matcher = ResumeMatcher(self)
        
        match_data = await matcher.match(
            resume_text=resume_text,
            job_title=job_title,
            job_description=job_description,
            job_requirements=job_requirements
        )
        
        gap_data = await matcher.analyze_skill_gap(
            candidate_skills=resume_text[:2000],
            job_requirements=job_requirements
        )
        
        q_gen = QuestionGenerator(self)
        q_data = await q_gen.generate_questions(
            job_description=job_description,
            resume_text=resume_text,
            skill_gaps=gap_data
        )
        
        return ResumeMatchResult(
            score=match_data.get("score", 50.0),
            fit_explanation=match_data.get("fit_explanation", ""),
            skill_gap=gap_data,
            suggested_questions=q_data.get("questions", [])
        )

    async def generate_email(self, template_type: str, candidate_name: str, job_title: str, recruiter_name: str) -> Dict[str, str]:
        from app.ai.emails.email_generator import EmailGenerator
        email_gen = EmailGenerator(self)
        return await email_gen.generate_email(
            template_type=template_type,
            candidate_name=candidate_name,
            job_title=job_title,
            recruiter_name=recruiter_name
        )

    async def chat_interaction(self, query: str, context: str) -> str:
        prompt = f"""
        You are HireMind AI Assistant. Help the recruiter answer their query using the context below.
        Context:
        {context}

        Recruiter Query:
        {query}
        """
        return await self.call_llm(prompt)


    def _mock_response(self, prompt: str) -> str:
        """Returns mock responses matching prompt context patterns for local developer runs."""
        prompt_upper = prompt.upper()
        if "PARSE" in prompt_upper or "EXTRACT" in prompt_upper:
            return json.dumps({
                "candidate_info": {
                    "first_name": "Rounak",
                    "last_name": "Mishra",
                    "email": "mishra.rounak15@gmail.com",
                    "phone": "+91-9876543210"
                },
                "skills": ["Python", "FastAPI", "React", "PostgreSQL", "Docker", "Git"],
                "experience": [
                    {
                        "job_title": "Software Engineer",
                        "company": "HireMind Org",
                        "dates": "2023 - Present",
                        "description": "Full-stack development using FastAPI, React, and PostgreSQL."
                    }
                ],
                "education": [
                    {
                        "degree": "Bachelor of Technology",
                        "school": "KIIT University",
                        "field_of_study": "Computer Science",
                        "graduation_year": 2023
                    }
                ],
                "projects": [
                    {
                        "title": "HireMind AI",
                        "description": "AI-powered Applicant Tracking System backend and frontend."
                    }
                ],
                "certifications": ["AWS Certified Cloud Practitioner"],
                "companies": ["HireMind Org"],
                "designation": "Software Engineer",
                "links": ["https://github.com/rounakm535", "https://linkedin.com/in/rounakm535"],
                "summary": "Full Stack developer with specialization in FastAPI backends and React frontends."
            })
        elif "MATCH" in prompt_upper or "COMPARE" in prompt_upper:
            return json.dumps({
                "score": 88.0,
                "matching_skills": ["Python", "FastAPI", "React", "PostgreSQL"],
                "missing_skills": ["Redis", "Qdrant"],
                "experience_match": "Strong fit - candidate has worked for 3 years building API services.",
                "education_match": "Matches - holds B.Tech in Computer Science.",
                "hiring_recommendation": "Highly Recommended. Proceed to technical screen round."
            })
        elif "RANK" in prompt_upper:
            return json.dumps({
                "rankings": [],
                "reasoning": "Standard ranking sort ordering."
            })
        elif "GAP" in prompt_upper or "SKILL" in prompt_upper:
            return json.dumps({
                "missing_skills": ["Redis", "Qdrant"],
                "recommended_learning": ["Study vector database indices", "Redis pub-sub configurations"],
                "priority_skills": ["Qdrant embeddings storage"],
                "strengths": ["Excellent FastAPI and React capabilities"],
                "weaknesses": ["Lack of hands-on experience with vector search engines"]
            })
        elif "SUMMARY" in prompt_upper:
            return "Rounak Mishra is an experienced Full-Stack Developer with hands-on proficiency in FastAPI and React."
        elif "QUESTION" in prompt_upper or "INTERVIEW" in prompt_upper:
            return json.dumps({
                "questions": [
                    {
                        "question": "How do you implement dependency injection in FastAPI, and what are its core advantages?",
                        "expected_answer": "By using the Depends() class. It helps with decoupled parameters, testability, and database session bindings.",
                        "category": "Technical",
                        "difficulty_level": "Medium"
                    },
                    {
                        "question": "Can you describe a challenging bug you fixed in a React application?",
                        "expected_answer": "Candidate should explain memory leaks in useEffect, state race conditions, or performance optimizations using useMemo.",
                        "category": "Behavioral",
                        "difficulty_level": "Hard"
                    }
                ]
            })
        elif "EMAIL" in prompt_upper or "INVITATION" in prompt_upper or "REJECTION" in prompt_upper:
            return json.dumps({
                "subject": "Interview Invitation - HireMind AI",
                "body": "Hello candidate,\n\nWe would love to invite you for an interview.\n\nBest regards,\nHireMind Team"
            })
        return "{}"
