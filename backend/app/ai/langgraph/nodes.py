from typing import Any, Dict
from app.ai.gemini_client import GeminiClient
from app.ai.langgraph.state import ScreenResumeState

# Instantiate Gemini Client
gemini_client = GeminiClient()


async def resume_parsing_node(state: ScreenResumeState) -> Dict[str, Any]:
    try:
        raw_text = state.get("resume_raw_text", "")
        parsed = await gemini_client.parse_resume(raw_text)
        return {"parsed_resume": parsed.model_dump()}
    except Exception as e:
        return {"errors": [f"Parsing error: {str(e)}"]}


async def embedding_generation_node(state: ScreenResumeState) -> Dict[str, Any]:
    # Mocking embedding generation interface (for storing in Qdrant later)
    mock_embeddings = [0.15] * 128
    return {"embeddings": mock_embeddings}


async def resume_matching_node(state: ScreenResumeState) -> Dict[str, Any]:
    try:
        raw_text = state.get("resume_raw_text", "")
        title = state.get("job_title", "")
        reqs = state.get("job_requirements", "")
        desc = state.get("job_description", "")
        
        match_result = await gemini_client.match_resume(
            resume_text=raw_text,
            job_title=title,
            job_requirements=reqs,
            job_description=desc
        )
        return {
            "match_score": match_result.score,
            "fit_explanation": match_result.fit_explanation,
            "skill_gap": match_result.skill_gap,
            "suggested_questions": match_result.suggested_questions
        }
    except Exception as e:
        return {"errors": [f"Matching error: {str(e)}"]}


async def skill_gap_analysis_node(state: ScreenResumeState) -> Dict[str, Any]:
    # Skill gap is already generated in the resume_matching_node, 
    # but we represent the node here for architectural compliance.
    # If not present, we can compute it.
    if state.get("skill_gap"):
        return {}
    
    try:
        parsed = state.get("parsed_resume") or {}
        candidate_skills = parsed.get("skills", [])
        reqs = state.get("job_requirements", "")
        
        # Call Gemini Skill Gap directly
        prompt = f"Analyze skill gaps between Job Requirements: {reqs} and Candidate Skills: {candidate_skills}. Return JSON keys: matched_skills, missing_skills, additional_skills."
        response = await gemini_client._call_llm(prompt)
        import json
        gap_data = json.loads(gemini_client._clean_json_response(response))
        return {"skill_gap": gap_data}
    except Exception as e:
        return {"errors": [f"Skill gap error: {str(e)}"]}


async def candidate_ranking_node(state: ScreenResumeState) -> Dict[str, Any]:
    # Architectural ranking node.
    # In a full run, we would rank this candidate against other resumes in the database.
    # Here we mock this ranking step.
    return {"rankings": ["current-candidate-id-ranked-first"]}


async def interview_question_generation_node(state: ScreenResumeState) -> Dict[str, Any]:
    if state.get("suggested_questions"):
        return {}

    try:
        raw_text = state.get("resume_raw_text", "")
        desc = state.get("job_description", "")
        gap = state.get("skill_gap") or {}
        
        prompt = f"Generate 3 interview questions based on Resume: {raw_text[:2000]} and Job Description: {desc} and Skill Gaps: {gap}. Return JSON with key 'questions' containing list of objects (question, expected_answer, category)."
        response = await gemini_client._call_llm(prompt)
        import json
        q_data = json.loads(gemini_client._clean_json_response(response))
        return {"suggested_questions": q_data.get("questions", [])}
    except Exception as e:
        return {"errors": [f"Interview question error: {str(e)}"]}


async def summary_generation_node(state: ScreenResumeState) -> Dict[str, Any]:
    try:
        raw_text = state.get("resume_raw_text", "")
        prompt = f"Summarize this resume for a recruiter: {raw_text[:3000]}"
        summary_text = await gemini_client._call_llm(prompt)
        return {"summary": summary_text}
    except Exception as e:
        return {"errors": [f"Summary generation error: {str(e)}"]}
