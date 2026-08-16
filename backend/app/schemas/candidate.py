import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from app.models.candidate import CandidateStatus
from app.schemas.resume import ResumeResponse, MatchScoreResponse


class SkillBase(BaseModel):
    name: str


class SkillCreate(SkillBase):
    pass


class SkillResponse(SkillBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID


class CandidateSkillBase(BaseModel):
    proficiency: Optional[str] = None


class CandidateSkillCreate(CandidateSkillBase):
    skill_name: str


class CandidateSkillResponse(CandidateSkillBase):
    model_config = ConfigDict(from_attributes=True)

    skill: SkillResponse


class CandidateBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    status: CandidateStatus = CandidateStatus.NEW


class CandidateCreate(CandidateBase):
    skills: Optional[List[CandidateSkillCreate]] = None


class CandidateUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    status: Optional[CandidateStatus] = None
    skills: Optional[List[CandidateSkillCreate]] = None


class CandidateResponse(CandidateBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    organization_id: uuid.UUID
    candidate_skills: List[CandidateSkillResponse] = []
    resumes: List[ResumeResponse] = []
    match_scores: List[MatchScoreResponse] = []
    created_at: datetime
    updated_at: datetime

