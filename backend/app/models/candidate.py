import enum
import uuid
from typing import List, Optional
from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
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

    candidate_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("candidates.id", ondelete="CASCADE"), primary_key=True
    )
    skill_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True
    )
    proficiency: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Relationships
    candidate: Mapped["Candidate"] = relationship("Candidate", back_populates="candidate_skills")
    skill: Mapped["Skill"] = relationship("Skill", back_populates="candidate_skills")


class Candidate(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "candidates"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    status: Mapped[CandidateStatus] = mapped_column(
        Enum(CandidateStatus), default=CandidateStatus.NEW, nullable=False
    )

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="candidates")
    resumes: Mapped[List["Resume"]] = relationship(
        "Resume", back_populates="candidate", cascade="all, delete-orphan"
    )
    match_scores: Mapped[List["MatchScore"]] = relationship(
        "MatchScore", back_populates="candidate", cascade="all, delete-orphan"
    )
    candidate_skills: Mapped[List["CandidateSkill"]] = relationship(
        "CandidateSkill", back_populates="candidate", cascade="all, delete-orphan"
    )
