import json
import re
import logging
from typing import Any, Dict, List
from app.ai.prompts.match_prompt import RESUME_MATCHING_PROMPT, SKILL_GAP_PROMPT, FULL_SCREENING_PROMPT
from app.ai.parser.resume_parser import SKILL_VOCABULARY

logger = logging.getLogger(__name__)


class ResumeMatcher:
    def __init__(self, gemini_client):
        self.gemini_client = gemini_client

    async def full_screen(
        self, resume_text: str, job_title: str, job_description: str, job_requirements: str
    ) -> Dict[str, Any]:
        """Perform unified single-pass AI screening and matching."""
        prompt = FULL_SCREENING_PROMPT.format(
            job_title=job_title,
            job_description=job_description,
            job_requirements=job_requirements,
            resume_text=resume_text[:4000],
        )
        try:
            response_text = await self.gemini_client.call_llm(prompt)
            clean_json = self._clean_json(response_text)
            parsed = json.loads(clean_json)
            if isinstance(parsed, dict) and "score" in parsed:
                return self._normalize_screening_result(parsed, resume_text, job_title, job_requirements)
            return self.heuristic_screen(resume_text, job_title, job_description, job_requirements)
        except Exception as e:
            logger.warning(f"Full screening JSON parsing error ({e}); using heuristic screening.")
            return self.heuristic_screen(resume_text, job_title, job_description, job_requirements)

    def _normalize_screening_result(
        self, data: Dict[str, Any], resume_text: str, job_title: str, job_requirements: str
    ) -> Dict[str, Any]:
        score = float(data.get("score", 75.0))
        # Ensure score is within valid bounds
        score = max(10.0, min(100.0, score))
        data["score"] = round(score, 1)

        if not data.get("fit_explanation"):
            data["fit_explanation"] = f"Candidate demonstrates relevant qualifications for the {job_title} role."

        if "matching_skills" not in data or not data["matching_skills"]:
            heur = self.heuristic_screen(resume_text, job_title, "", job_requirements)
            data["matching_skills"] = heur["matching_skills"]
            data["missing_skills"] = heur["missing_skills"]
            data["additional_skills"] = heur["additional_skills"]

        if "suggested_questions" not in data or not data["suggested_questions"]:
            data["suggested_questions"] = self._default_questions(job_title, data.get("matching_skills", []))

        return data

    def heuristic_screen(
        self, resume_text: str, job_title: str, job_description: str, job_requirements: str
    ) -> Dict[str, Any]:
        """Fast, intelligent deterministic screening engine based on semantic keyword overlap."""
        resume_lower = f" {resume_text.lower()} "
        job_combined = f" {job_title.lower()} {job_description.lower()} {job_requirements.lower()} "

        # Extract skills present in resume
        candidate_skills = []
        for skill in SKILL_VOCABULARY:
            pattern = r'(?<!\w)' + re.escape(skill.lower()) + r'(?!\w)'
            if re.search(pattern, resume_lower):
                candidate_skills.append(skill)

        # Extract skills mentioned in job posting
        job_skills = []
        for skill in SKILL_VOCABULARY:
            pattern = r'(?<!\w)' + re.escape(skill.lower()) + r'(?!\w)'
            if re.search(pattern, job_combined):
                job_skills.append(skill)

        # If job didn't specify explicit skills from vocabulary, extract keywords
        if not job_skills:
            job_skills = ["Technical Problem Solving", "Software Engineering", "Communication"]

        # Intersect
        matching = [s for s in job_skills if s in candidate_skills]
        missing = [s for s in job_skills if s not in candidate_skills]
        additional = [s for s in candidate_skills if s not in job_skills][:8]

        # Calculate score
        if job_skills:
            skill_ratio = len(matching) / len(job_skills)
        else:
            skill_ratio = 0.75

        base_score = 40.0 + (skill_ratio * 45.0)
        # Bonus for experience keyword matches
        if any(w in resume_lower for w in ["lead", "senior", "principal", "architect", "engineer", "developer"]):
            base_score += 10.0
        if any(w in resume_lower for w in ["bachelor", "master", "degree", "university", "b.s.", "m.s."]):
            base_score += 5.0

        final_score = round(max(35.0, min(96.0, base_score)), 1)

        # Explanation
        matching_str = ", ".join(matching[:4]) if matching else "core engineering foundations"
        missing_str = f" However, key desired skills like {', '.join(missing[:3])} were not explicitly identified." if missing else " The candidate covers all required core competencies."

        fit_explanation = (
            f"The candidate is a strong fit for the {job_title} role with an evaluated match score of {final_score}%. "
            f"They bring direct proficiency in {matching_str}.{missing_str} "
            f"Overall background demonstrates solid domain expertise and relevant project experience."
        )

        return {
            "score": final_score,
            "fit_explanation": fit_explanation,
            "matching_skills": matching,
            "missing_skills": missing,
            "additional_skills": additional,
            "strengths": [f"Demonstrated proficiency in {s}" for s in matching[:3]] or ["Solid background fundamentals"],
            "weaknesses": [f"Missing direct experience in {s}" for s in missing[:3]] or ["No critical skill gaps identified"],
            "recommended_learning": [f"Familiarization with {s}" for s in missing[:3]] or ["Advanced architectural patterns"],
            "suggested_questions": self._default_questions(job_title, matching),
        }

    def _default_questions(self, job_title: str, matching_skills: List[str]) -> List[Dict[str, str]]:
        top_skill = matching_skills[0] if matching_skills else "Python"
        second_skill = matching_skills[1] if len(matching_skills) > 1 else "microservice architectures"
        return [
            {
                "question": f"How do you design scalable applications utilizing {top_skill} and optimize for high throughput?",
                "expected_answer": f"Candidate should discuss concurrency, memory management, profiling tools, and best practices in {top_skill}.",
                "category": "Technical",
                "difficulty_level": "Medium"
            },
            {
                "question": f"Can you describe a production challenge you resolved involving {second_skill}?",
                "expected_answer": "Candidate should explain root cause identification, architectural trade-offs, and verification of the fix.",
                "category": "Technical",
                "difficulty_level": "Medium"
            },
            {
                "question": "How do you approach cross-functional communication and code review in an agile team?",
                "expected_answer": "Candidate should demonstrate constructive review practices, clear documentation, and empathy.",
                "category": "Behavioral",
                "difficulty_level": "Easy"
            }
        ]

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
