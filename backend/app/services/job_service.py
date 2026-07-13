import uuid
from typing import Optional
from app.models.job import Job, JobType, JobStatus
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobCreate, JobUpdate
from app.utils.pagination import PaginationParams, Page
from app.exceptions.custom import EntityNotFoundError


class JobService:
    def __init__(self, job_repo: JobRepository):
        self.job_repo = job_repo

    async def get_job_by_id(self, job_id: uuid.UUID, organization_id: uuid.UUID) -> Job:
        job = await self.job_repo.get_by_id(job_id)
        if not job or job.organization_id != organization_id:
            raise EntityNotFoundError(f"Job with ID {job_id} not found under this organization.")
        return job

    async def create_job(self, schema: JobCreate, organization_id: uuid.UUID) -> Job:
        job = Job(
            organization_id=organization_id,
            title=schema.title,
            description=schema.description,
            requirements=schema.requirements,
            location=schema.location,
            job_type=schema.job_type,
            status=schema.status,
        )
        return await self.job_repo.create(job)

    async def update_job(self, job_id: uuid.UUID, schema: JobUpdate, organization_id: uuid.UUID) -> Job:
        job = await self.get_job_by_id(job_id, organization_id)

        update_data = schema.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(job, key, value)

        return await self.job_repo.update(job)

    async def delete_job(self, job_id: uuid.UUID, organization_id: uuid.UUID) -> None:
        job = await self.get_job_by_id(job_id, organization_id)
        await self.job_repo.delete(job)

    async def list_jobs(
        self,
        organization_id: uuid.UUID,
        params: PaginationParams,
        job_type: Optional[JobType] = None,
        status: Optional[JobStatus] = None,
        search: Optional[str] = None,
    ) -> Page[Job]:
        items, total = await self.job_repo.list_jobs(
            organization_id=organization_id,
            skip=params.offset,
            limit=params.limit,
            job_type=job_type,
            status=status,
            search=search,
        )
        return Page.create(items=items, total=total, params=params)
