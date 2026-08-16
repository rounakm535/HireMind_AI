import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict


class InterviewQuestionBase(BaseModel):
    question: str
    expected_answer: Optional[str] = None
    category: Optional[str] = None


class InterviewQuestionCreate(InterviewQuestionBase):
    pass


class InterviewQuestionResponse(InterviewQuestionBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    resume_id: uuid.UUID
    created_at: datetime


class ResumeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    candidate_id: uuid.UUID
    file_url: str
    file_name: str
    parsed_content: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None
    interview_questions: List[InterviewQuestionResponse] = []
    created_at: datetime
    updated_at: datetime


class MatchScoreResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    job_id: uuid.UUID
    candidate_id: uuid.UUID
    resume_id: uuid.UUID
    score: float
    fit_explanation: Optional[str] = None
    skill_gap_analysis: Optional[Dict[str, Any]] = None
    created_at: datetime


class EmailLogCreate(BaseModel):
    recipient_email: str
    subject: str
    body: str


class EmailLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    sender_id: Optional[uuid.UUID] = None
    recipient_email: str
    subject: str
    body: str
    status: str
    created_at: datetime



class ResumeParsingResult(BaseModel):
    model_config = ConfigDict(extra="allow")

    candidate_info: Dict[str, Any]
    skills: List[str]
    experience: List[Dict[str, Any]]
    education: List[Dict[str, Any]]
    summary: str
    projects: Optional[List[Dict[str, Any]]] = None
    certifications: Optional[List[str]] = None
    designation: Optional[str] = None
    links: Optional[List[str]] = None



class ResumeMatchResult(BaseModel):
    score: float
    fit_explanation: str
    skill_gap: Dict[str, Any]
    suggested_questions: List[Dict[str, str]]
