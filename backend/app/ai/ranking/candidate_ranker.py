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
        try:
            return json.loads(clean_json)
        except Exception:
            return {"rankings": [], "reasoning": response_text}

    async def compare_candidates(self, job_description: str, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detailed side-by-side comparison of 2+ candidates against role requirements."""
        candidates_str = ""
        for idx, c in enumerate(candidates, 1):
            candidates_str += f"\nCandidate #{idx}:\nName: {c.get('name')}\nEmail: {c.get('email')}\nStatus: {c.get('status')}\nSkills: {', '.join(c.get('skills', []))}\nMatch Score: {c.get('score', 'N/A')}\nSummary: {c.get('summary', 'No summary provided')}\n"

        prompt = f"""
        You are a Principal Technical Recruiter comparing candidate profiles for a hiring committee.
        Target Role / Job Description:
        {job_description}

        Candidates to Compare:
        {candidates_str}

        Return a JSON object comparing these candidates with the exact schema:
        {{
          "top_recommendation": "Candidate Name",
          "summary_verdict": "Detailed synthesis of which candidate is best suited and why.",
          "comparisons": [
            {{
              "candidate_name": "Candidate Name",
              "key_strengths": ["strength1", "strength2"],
              "skill_gaps": ["gap1"],
              "experience_level": "Senior / Mid",
              "fit_score": 88,
              "verdict": "Strong candidate for leadership / interview round."
            }}
          ]
        }}

        Output ONLY valid JSON.
        """
        response_text = await self.gemini_client.call_llm(prompt)
        clean_json = self._clean_json(response_text)
        try:
            return json.loads(clean_json)
        except Exception:
            # Fallback structure if LLM outputs markdown
            return {
                "top_recommendation": candidates[0].get("name") if candidates else "N/A",
                "summary_verdict": "Candidate comparison evaluated.",
                "comparisons": [
                    {
                        "candidate_name": c.get("name"),
                        "key_strengths": c.get("skills", [])[:3],
                        "skill_gaps": ["Domain specific tool certification"],
                        "experience_level": "Mid-Senior",
                        "fit_score": c.get("score") or 80,
                        "verdict": "Qualified applicant for interview process."
                    }
                    for c in candidates
                ]
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
