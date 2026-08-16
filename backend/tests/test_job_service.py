import pytest
import uuid
from app.db.database import AsyncSessionLocal, init_db
from app.repositories.job_repository import JobRepository
from app.repositories.user_repository import UserRepository
from app.services.job_service import JobService
from app.schemas.job import JobCreate, JobUpdate
from app.models.job import JobType, JobStatus
from app.utils.pagination import PaginationParams
from app.exceptions.custom import EntityNotFoundError


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    import asyncio
    asyncio.run(init_db())


@pytest.mark.asyncio
async def test_job_service_crud_operations():
    async with AsyncSessionLocal() as session:
        user_repo = UserRepository(session)
        job_repo = JobRepository(session)
        job_service = JobService(job_repo)

        # Create organization
        org = await user_repo.create_organization(f"Org_{uuid.uuid4().hex[:6]}")
        org_id = org.id

        # 1. Create Job
        create_schema = JobCreate(
            title="Senior Full Stack Engineer",
            description="Leading full stack web & AI development",
            requirements="Python, FastAPI, React, TypeScript",
            location="Remote",
            job_type=JobType.FULL_TIME,
            status=JobStatus.OPEN,
        )
        job = await job_service.create_job(create_schema, org_id)
        assert job.id is not None
        assert job.title == "Senior Full Stack Engineer"
        assert job.organization_id == org_id

        # 2. Get Job by ID
        fetched_job = await job_service.get_job_by_id(job.id, org_id)
        assert fetched_job.id == job.id

        # 3. Update Job
        update_schema = JobUpdate(title="Principal Full Stack Engineer", status=JobStatus.OPEN)
        updated_job = await job_service.update_job(job.id, update_schema, org_id)
        assert updated_job.title == "Principal Full Stack Engineer"

        # 4. List Jobs
        params = PaginationParams(page=1, size=10)
        page = await job_service.list_jobs(org_id, params, status=JobStatus.OPEN)
        assert page.total >= 1
        assert any(item.id == job.id for item in page.items)

        # 5. Delete Job
        await job_service.delete_job(job.id, org_id)
        with pytest.raises(EntityNotFoundError):
            await job_service.get_job_by_id(job.id, org_id)
