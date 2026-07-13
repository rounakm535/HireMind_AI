import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy import ForeignKey, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base, UUIDMixin, TimestampMixin


class Resume(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "resumes"

    candidate_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False
    )
    file_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    parsed_content: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    raw_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    candidate: Mapped["Candidate"] = relationship("Candidate", back_populates="resumes")
    interview_questions: Mapped[List["InterviewQuestion"]] = relationship(
        "InterviewQuestion", back_populates="resume", cascade="all, delete-orphan"
    )
    match_scores: Mapped[List["MatchScore"]] = relationship(
        "MatchScore", back_populates="resume", cascade="all, delete-orphan"
    )


class InterviewQuestion(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "interview_questions"

    resume_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False
    )
    question: Mapped[str] = mapped_column(Text, nullable=False)
    expected_answer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Relationships
    resume: Mapped["Resume"] = relationship("Resume", back_populates="interview_questions")
