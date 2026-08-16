import uuid
from sqlalchemy import Float, ForeignKey, String, Text, JSON
from sqlalchemy.orm import mapped_column, relationship
from app.db.database import Base, UUIDMixin, TimestampMixin
from app.models.user import User

class MatchScore(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "match_scores"

    job_id = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False
    )
    candidate_id = mapped_column(
        ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False
    )
    resume_id = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False
    )
    score = mapped_column(Float, nullable=False)
    fit_explanation = mapped_column(Text, nullable=True)
    skill_gap_analysis = mapped_column(JSON, nullable=True)

    # Relationships
    job = relationship("Job", back_populates="match_scores")
    candidate = relationship("Candidate", back_populates="match_scores")
    resume = relationship("Resume", back_populates="match_scores")


class EmailLog(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "email_logs"

    sender_id = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    recipient_email = mapped_column(String(255), nullable=False)
    subject = mapped_column(String(255), nullable=False)
    body = mapped_column(Text, nullable=False)
    status = mapped_column(String(50), default="SENT", nullable=False)  # SENT, FAILED, PENDING

    # Relationships
    sender = relationship("User", back_populates="email_logs")
