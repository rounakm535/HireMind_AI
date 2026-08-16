import pytest
import uuid
from app.db.database import AsyncSessionLocal, init_db
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.user_repository import UserRepository
from app.services.candidate_service import CandidateService
from app.schemas.candidate import CandidateCreate, CandidateUpdate, CandidateSkillCreate
from app.models.candidate import CandidateStatus
from app.utils.pagination import PaginationParams
from app.exceptions.custom import EntityNotFoundError


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    import asyncio
    asyncio.run(init_db())


@pytest.mark.asyncio
async def test_candidate_service_crud_operations():
    async with AsyncSessionLocal() as session:
        user_repo = UserRepository(session)
        cand_repo = CandidateRepository(session)
        cand_service = CandidateService(cand_repo)

        # Create organization
        org = await user_repo.create_organization(f"Org_{uuid.uuid4().hex[:6]}")
        org_id = org.id

        # 1. Create Candidate with Skills
        cand_schema = CandidateCreate(
            first_name="Jane",
            last_name="Doe",
            email=f"jane_{uuid.uuid4().hex[:6]}@example.com",
            phone="+15551234567",
            status=CandidateStatus.NEW,
            skills=[
                CandidateSkillCreate(skill_name="Python", proficiency="Expert"),
                CandidateSkillCreate(skill_name="FastAPI", proficiency="Intermediate"),
            ],
        )

        candidate = await cand_service.create_candidate(cand_schema, org_id)
        assert candidate.id is not None
        assert candidate.first_name == "Jane"
        assert candidate.organization_id == org_id
        assert len(candidate.candidate_skills) == 2

        # 2. Get Candidate by ID
        fetched = await cand_service.get_candidate_by_id(candidate.id, org_id)
        assert fetched.id == candidate.id

        # 3. Update Candidate
        update_schema = CandidateUpdate(status=CandidateStatus.SCREENING)
        updated = await cand_service.update_candidate(candidate.id, update_schema, org_id)
        assert updated.status == CandidateStatus.SCREENING

        # 4. List Candidates
        params = PaginationParams(page=1, size=10)
        page = await cand_service.list_candidates(org_id, params, status=CandidateStatus.SCREENING)
        assert page.total >= 1

        # 5. Delete Candidate
        await cand_service.delete_candidate(candidate.id, org_id)
        with pytest.raises(EntityNotFoundError):
            await cand_service.get_candidate_by_id(candidate.id, org_id)
