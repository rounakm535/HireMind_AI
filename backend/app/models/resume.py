import uuid
from sqlalchemy import ForeignKey, String, Text, JSON
from sqlalchemy.orm import mapped_column, relationship
from app.db.database import Base, UUIDMixin, TimestampMixin

class Resume(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "resumes"

    candidate_id = mapped_column(
        ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False
    )
    file_url = mapped_column(String(1000), nullable=False)
    file_name = mapped_column(String(255), nullable=False)
    parsed_content = mapped_column(JSON, nullable=True)
    raw_text = mapped_column(Text, nullable=True)
    summary = mapped_column(Text, nullable=True)

    # Relationships
    candidate = relationship("Candidate", back_populates="resumes")
    interview_questions = relationship(
        "InterviewQuestion", back_populates="resume", cascade="all, delete-orphan"
    )
    match_scores = relationship(
        "MatchScore", back_populates="resume", cascade="all, delete-orphan"
    )


class InterviewQuestion(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "interview_questions"

    resume_id = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False
    )
    question = mapped_column(Text, nullable=False)
    expected_answer = mapped_column(Text, nullable=True)
    category = mapped_column(String(100), nullable=True)

    # Relationships
    resume = relationship("Resume", back_populates="interview_questions")
