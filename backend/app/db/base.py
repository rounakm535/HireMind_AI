# Import all models for Alembic import discovery
from app.db.database import Base
from app.models.organization import Organization
from app.models.user import User, AuditLog
from app.models.job import Job
from app.models.candidate import Candidate, CandidateSkill
from app.models.skill import Skill
from app.models.resume import Resume, InterviewQuestion
from app.models.match import MatchScore, EmailLog
