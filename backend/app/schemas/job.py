import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.models.job import JobStatus, JobType


class JobBase(BaseModel):
    title: str
    description: str
    requirements: str
    location: str
    job_type: JobType = JobType.FULL_TIME
    status: JobStatus = JobStatus.DRAFT


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[JobType] = None
    status: Optional[JobStatus] = None


class JobResponse(JobBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    organization_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

