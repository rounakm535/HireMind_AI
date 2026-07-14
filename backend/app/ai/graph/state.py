from typing import Any, Dict, List, Optional, TypedDict

class ScreenResumeState(TypedDict):
    # Core inputs
    resume_id: Optional[str]
    candidate_id: Optional[str]
    organization_id: Optional[str]
    job_id: Optional[str]
    
    resume_raw_text: str
    job_title: str
    job_description: str
    job_requirements: str

    # Pipeline intermediates/outputs
    parsed_resume: Optional[Dict[str, Any]]
    embeddings: Optional[List[float]]
    similar_candidates: Optional[List[Dict[str, Any]]]
    match_score: Optional[float]
    fit_explanation: Optional[str]
    matching_skills: Optional[List[str]]
    missing_skills: Optional[List[str]]
    experience_match: Optional[str]
    education_match: Optional[str]
    hiring_recommendation: Optional[str]
    
    skill_gap: Optional[Dict[str, Any]]
    suggested_questions: Optional[List[Dict[str, Any]]]
    summary: Optional[str]
    rankings: Optional[List[Dict[str, Any]]]
    
    # State tracking
    retry_count: int
    errors: Optional[List[str]]
