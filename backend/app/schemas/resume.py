import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class InterviewQuestionBase(BaseModel):
    question: str
    expected_answer: Optional[str] = None
    category: Optional[str] = None


class InterviewQuestionCreate(InterviewQuestionBase):
    pass


class InterviewQuestionResponse(InterviewQuestionBase):
    id: uuid.UUID
    resume_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


class ResumeResponse(BaseModel):
    id: uuid.UUID
    candidate_id: uuid.UUID
    file_url: str
    file_name: str
    parsed_content: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MatchScoreResponse(BaseModel):
    id: uuid.UUID
    job_id: uuid.UUID
    candidate_id: uuid.UUID
    resume_id: uuid.UUID
    score: float
    fit_explanation: Optional[str] = None
    skill_gap_analysis: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class EmailLogCreate(BaseModel):
    recipient_email: str
    subject: str
    body: str


class EmailLogResponse(BaseModel):
    id: uuid.UUID
    sender_id: Optional[uuid.UUID] = None
    recipient_email: str
    subject: str
    body: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ResumeParsingResult(BaseModel):
    candidate_info: Dict[str, Any]
    skills: List[str]
    experience: List[Dict[str, Any]]
    education: List[Dict[str, Any]]
    summary: str


class ResumeMatchResult(BaseModel):
    score: float
    fit_explanation: str
    skill_gap: Dict[str, Any]
    suggested_questions: List[Dict[str, str]]
