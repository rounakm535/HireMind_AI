import enum
import uuid
from typing import List, Optional
from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import mapped_column, relationship
from app.db.database import Base, UUIDMixin, TimestampMixin

class CandidateStatus(str, enum.Enum):
    NEW = "NEW"
    SCREENING = "SCREENING"
    INTERVIEWING = "INTERVIEWING"
    OFFERED = "OFFERED"
    HIRED = "HIRED"
    REJECTED = "REJECTED"


class CandidateSkill(Base):
    __tablename__ = "candidate_skills"

    candidate_id = mapped_column(
        ForeignKey("candidates.id", ondelete="CASCADE"), primary_key=True
    )
    skill_id = mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True
    )
    proficiency = mapped_column(String(50), nullable=True)

    # Relationships
    candidate = relationship("Candidate", back_populates="candidate_skills")
    skill = relationship("Skill", back_populates="candidate_skills")


class Candidate(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "candidates"

    organization_id = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    first_name = mapped_column(String(100), nullable=False)
    last_name = mapped_column(String(100), nullable=False)
    email = mapped_column(String(255), index=True, nullable=False)
    phone = mapped_column(String(50), nullable=True)
    status = mapped_column(
        Enum(CandidateStatus), default=CandidateStatus.NEW, nullable=False
    )

    # Relationships
    organization = relationship("Organization", back_populates="candidates")
    resumes = relationship(
        "Resume", back_populates="candidate", cascade="all, delete-orphan"
    )
    match_scores = relationship(
        "MatchScore", back_populates="candidate", cascade="all, delete-orphan"
    )
    candidate_skills = relationship(
        "CandidateSkill", back_populates="candidate", cascade="all, delete-orphan"
    )
