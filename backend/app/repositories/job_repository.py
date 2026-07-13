import uuid
from typing import List, Optional, Tuple
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.job import Job, JobType, JobStatus


class JobRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, job_id: uuid.UUID) -> Optional[Job]:
        result = await self.db.execute(select(Job).where(Job.id == job_id))
        return result.scalars().first()

    async def create(self, job: Job) -> Job:
        self.db.add(job)
        await self.db.flush()
        return job

    async def update(self, job: Job) -> Job:
        self.db.add(job)
        await self.db.flush()
        return job

    async def delete(self, job: Job) -> None:
        await self.db.delete(job)
        await self.db.flush()

    async def list_jobs(
        self,
        organization_id: uuid.UUID,
        skip: int = 0,
        limit: int = 20,
        job_type: Optional[JobType] = None,
        status: Optional[JobStatus] = None,
        search: Optional[str] = None,
    ) -> Tuple[List[Job], int]:
        # Build query
        query = select(Job).where(Job.organization_id == organization_id)

        if job_type:
            query = query.where(Job.job_type == job_type)
        if status:
            query = query.where(Job.status == status)
        if search:
            query = query.where(
                or_(
                    Job.title.ilike(f"%{search}%"),
                    Job.description.ilike(f"%{search}%"),
                    Job.requirements.ilike(f"%{search}%"),
                )
            )

        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar_one()

        # Retrieve items
        query = query.order_by(Job.created_at.desc()).offset(skip).limit(limit)
        items_result = await self.db.execute(query)
        items = list(items_result.scalars().all())

        return items, total
