from sqlalchemy import String
from sqlalchemy.orm import mapped_column, relationship
from app.db.database import Base, UUIDMixin, TimestampMixin


class Skill(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "skills"

    name = mapped_column(String(100), unique=True, index=True, nullable=False)

    # Relationships
    candidate_skills = relationship(
        "CandidateSkill", back_populates="skill", cascade="all, delete"
    )
