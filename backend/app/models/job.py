import enum
import uuid
from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import mapped_column, relationship
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

    organization_id = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    title = mapped_column(String(255), index=True, nullable=False)
    description = mapped_column(Text, nullable=False)
    requirements = mapped_column(Text, nullable=False)
    location = mapped_column(String(255), nullable=False)
    job_type = mapped_column(
        Enum(JobType), default=JobType.FULL_TIME, nullable=False
    )
    status = mapped_column(
        Enum(JobStatus), default=JobStatus.DRAFT, nullable=False
    )

    # Relationships
    organization = relationship("Organization", back_populates="jobs")
    match_scores = relationship(
        "MatchScore", back_populates="job", cascade="all, delete-orphan"
    )
