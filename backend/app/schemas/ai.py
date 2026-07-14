from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class ParseRequest(BaseModel):
    raw_text: str

class MatchRequest(BaseModel):
    resume_text: str
    job_title: str
    job_description: str
    job_requirements: str

class RankRequest(BaseModel):
    job_description: str
    candidates: List[Dict[str, Any]]

class SummaryRequest(BaseModel):
    resume_text: str

class QuestionsRequest(BaseModel):
    job_description: str
    resume_text: str
    skill_gaps: Dict[str, Any]

class ChatRequest(BaseModel):
    query: str

class EmailRequest(BaseModel):
    template_type: str
    candidate_name: str
    job_title: str
    recruiter_name: str
    additional_context: Optional[str] = ""
