from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base, UUIDMixin, TimestampMixin


class Skill(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "skills"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)

    # Relationships
    candidate_skills: Mapped[List["CandidateSkill"]] = relationship(
        "CandidateSkill", back_populates="skill", cascade="all, delete"
    )
