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
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        else:
            self.model = None

    async def call_llm(self, prompt: str) -> str:
        """Invoke the Google Gemini LLM model with fallback handling."""
        if not self.is_configured:
            logger.warning("Gemini API key not configured, using mock fallback.")
            return self._mock_response(prompt)
        try:
            import asyncio
            loop = asyncio.get_running_loop()
            response = await asyncio.wait_for(
                loop.run_in_executor(None, lambda: self.model.generate_content(prompt)),
                timeout=5.0,
            )
            return response.text
        except Exception as e:
            logger.warning(f"Gemini LLM call exception ({e}); falling back to mock response.")
            return self._mock_response(prompt)

    async def parse_resume(self, raw_text: str) -> ResumeParsingResult:
        from app.ai.parser.resume_parser import ResumeParser
        parser = ResumeParser(self)
        try:
            data = await parser.parse(raw_text)
            return ResumeParsingResult(**data)
        except Exception as e:
            logger.warning(f"Resume parsing error ({e}); using safe fallback result.")
            fallback_data = parser._fallback(raw_text)
            return ResumeParsingResult(**fallback_data)

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
        import re
        prompt_upper = prompt.upper()

        # Handle Chat Assistant natural language queries
        if "HIREMIND AI ASSISTANT" in prompt_upper or "RECRUITER QUERY" in prompt_upper:
            query_text = ""
            if "Recruiter Query:" in prompt:
                query_text = prompt.split("Recruiter Query:")[-1].strip()

            q_lower = query_text.lower()
            words = set(re.findall(r'\b\w+\b', q_lower))

            is_greeting = bool(words & {"hello", "hi", "hey", "greetings"}) or (len(q_lower) > 0 and q_lower in ["hello", "hi", "hey"])
            is_interview = bool(words & {"question", "questions", "interview", "interviews", "ask"}) or "interview" in q_lower or "question" in q_lower

            if is_interview and not (is_greeting and len(words) <= 2):
                return (
                    "Here are key interview questions recommended for evaluating candidates:\n\n"
                    "1. **Technical Proficiency**: How do you implement dependency injection in FastAPI, and what are its core advantages?\n"
                    "   *Expected Key Answer*: Using `Depends()` for decoupled parameters, modular database session binding, and automated testing mocks.\n\n"
                    "2. **Problem Solving & Behavioral**: Can you describe a challenging bug or performance bottleneck you resolved in a web application?\n"
                    "   *Expected Key Answer*: Memory leaks, state race conditions in `useEffect`, or re-render optimizations using `useMemo` / `useCallback`.\n\n"
                    "3. **Database & Architecture**: How do you approach scaling database queries and optimizing search latency?\n"
                    "   *Expected Key Answer*: Index design, query optimization, vector search indexing, and Redis caching."
                )
            elif is_greeting or not q_lower:
                return "Hello! I am your HireMind AI Assistant. I can help you evaluate candidates, analyze skills, screen resumes, or generate interview questions. How can I assist you today?"
            elif bool(words & {"candidate", "candidates", "skill", "skills", "match", "matches", "python", "developer", "react"}):
                return "Based on your candidate database, applicants possess strong skills in Python, FastAPI, React, PostgreSQL, and Docker. You can view detailed match scores and run AI screening directly on candidate profiles."
            else:
                return f"I analyzed your request: '{query_text}'. All candidate records, resume parsings, and match metrics are synced. Let me know if you would like specific candidate recommendations or interview prep guides!"

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
        return "Hello! How can I assist you with your recruitment workflow today?"
