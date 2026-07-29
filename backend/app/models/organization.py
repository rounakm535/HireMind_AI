from sqlalchemy import String
from sqlalchemy.orm import mapped_column, relationship
from app.db.database import Base, UUIDMixin, TimestampMixin


class Organization(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "organizations"

    name = mapped_column(String(255), unique=True, index=True, nullable=False)

    # Relationships
    users = relationship(
        "User", back_populates="organization", cascade="all, delete-orphan"
    )
    jobs = relationship(
        "Job", back_populates="organization", cascade="all, delete-orphan"
    )
    candidates = relationship(
        "Candidate", back_populates="organization", cascade="all, delete-orphan"
    )
