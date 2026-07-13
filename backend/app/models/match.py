import uuid
from typing import Any, Dict, Optional
from sqlalchemy import Float, ForeignKey, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base, UUIDMixin, TimestampMixin


class MatchScore(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "match_scores"

    job_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False
    )
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False
    )
    resume_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False
    )
    score: Mapped[float] = mapped_column(Float, nullable=False)
    fit_explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    skill_gap_analysis: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    # Relationships
    job: Mapped["Job"] = relationship("Job", back_populates="match_scores")
    candidate: Mapped["Candidate"] = relationship("Candidate", back_populates="match_scores")
    resume: Mapped["Resume"] = relationship("Resume", back_populates="match_scores")


class EmailLog(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "email_logs"

    sender_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    recipient_email: Mapped[str] = mapped_column(String(255), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="SENT", nullable=False)  # SENT, FAILED, PENDING

    # Relationships
    sender: Mapped[Optional["User"]] = relationship("User", back_populates="email_logs")
