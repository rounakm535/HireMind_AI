from typing import Any, Dict, List, Optional, TypedDict


class ScreenResumeState(TypedDict):
    # Inputs
    resume_raw_text: str
    job_title: str
    job_description: str
    job_requirements: str

    # Intermediate / Outputs
    parsed_resume: Optional[Dict[str, Any]]
    embeddings: Optional[List[float]]
    match_score: Optional[float]
    fit_explanation: Optional[str]
    skill_gap: Optional[Dict[str, Any]]
    suggested_questions: Optional[List[Dict[str, Any]]]
    summary: Optional[str]
    rankings: Optional[List[str]]
    errors: Optional[List[str]]
