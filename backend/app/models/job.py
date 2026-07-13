import enum
import uuid
from typing import List, Optional
from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base, UUIDMixin, TimestampMixin


class JobType(str, enum.Enum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    CONTRACT = "CONTRACT"
    INTERN = "INTERN"
    REMOTE = "REMOTE"


class JobStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class Job(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "jobs"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    requirements: Mapped[str] = mapped_column(Text, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    job_type: Mapped[JobType] = mapped_column(
        Enum(JobType), default=JobType.FULL_TIME, nullable=False
    )
    status: Mapped[JobStatus] = mapped_column(
        Enum(JobStatus), default=JobStatus.DRAFT, nullable=False
    )

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="jobs")
    match_scores: Mapped[List["MatchScore"]] = relationship(
        "MatchScore", back_populates="job", cascade="all, delete-orphan"
    )
