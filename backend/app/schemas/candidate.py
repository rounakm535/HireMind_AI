import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from app.models.candidate import CandidateStatus


class SkillBase(BaseModel):
    name: str


class SkillCreate(SkillBase):
    pass


class SkillResponse(SkillBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class CandidateSkillBase(BaseModel):
    proficiency: Optional[str] = None


class CandidateSkillCreate(CandidateSkillBase):
    skill_name: str


class CandidateSkillResponse(CandidateSkillBase):
    skill: SkillResponse

    class Config:
        from_attributes = True


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
    id: uuid.UUID
    organization_id: uuid.UUID
    candidate_skills: List[CandidateSkillResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
