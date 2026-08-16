import uuid
from typing import Optional
from app.models.candidate import Candidate, CandidateStatus, CandidateSkill
from app.repositories.candidate_repository import CandidateRepository
from app.schemas.candidate import CandidateCreate, CandidateUpdate
from app.utils.pagination import PaginationParams, Page
from app.exceptions.custom import EntityNotFoundError


class CandidateService:
    def __init__(self, candidate_repo: CandidateRepository):
        self.candidate_repo = candidate_repo

    async def get_candidate_by_id(self, candidate_id: uuid.UUID, organization_id: uuid.UUID) -> Candidate:
        candidate = await self.candidate_repo.get_by_id(candidate_id)
        if not candidate or candidate.organization_id != organization_id:
            raise EntityNotFoundError(f"Candidate with ID {candidate_id} not found under this organization.")
        return candidate

    async def create_candidate(self, schema: CandidateCreate, organization_id: uuid.UUID) -> Candidate:
        # Check if candidate with same email already exists in this organization
        existing = await self.candidate_repo.get_by_email(schema.email, organization_id)
        if existing:
            existing.first_name = schema.first_name
            existing.last_name = schema.last_name
            if schema.phone:
                existing.phone = schema.phone
            created_candidate = await self.candidate_repo.update(existing)
        else:
            candidate = Candidate(
                organization_id=organization_id,
                first_name=schema.first_name,
                last_name=schema.last_name,
                email=schema.email,
                phone=schema.phone,
                status=schema.status,
            )
            created_candidate = await self.candidate_repo.create(candidate)

        # Handle skills association
        if schema.skills:
            for skill_item in schema.skills:
                skill = await self.candidate_repo.get_skill_by_name(skill_item.skill_name)
                if not skill:
                    skill = await self.candidate_repo.create_skill(skill_item.skill_name)
                
                cs = CandidateSkill(
                    candidate_id=created_candidate.id,
                    skill_id=skill.id,
                    proficiency=skill_item.proficiency,
                )
                await self.candidate_repo.add_candidate_skill(cs)

        # Refresh from database to get the preloaded skills
        return await self.candidate_repo.get_by_id(created_candidate.id)

    async def update_candidate(
        self, candidate_id: uuid.UUID, schema: CandidateUpdate, organization_id: uuid.UUID
    ) -> Candidate:
        candidate = await self.get_candidate_by_id(candidate_id, organization_id)

        update_data = schema.model_dump(exclude_unset=True)
        skills_data = update_data.pop("skills", None)

        for key, value in update_data.items():
            setattr(candidate, key, value)

        await self.candidate_repo.update(candidate)

        if skills_data is not None:
            # Clear old skills and insert new ones
            await self.candidate_repo.clear_candidate_skills(candidate_id)
            for skill_item in skills_data:
                # Resolve skill_item to dict if it was parsed as Pydantic model
                name = skill_item["skill_name"] if isinstance(skill_item, dict) else skill_item.skill_name
                prof = skill_item["proficiency"] if isinstance(skill_item, dict) else skill_item.proficiency

                skill = await self.candidate_repo.get_skill_by_name(name)
                if not skill:
                    skill = await self.candidate_repo.create_skill(name)

                cs = CandidateSkill(
                    candidate_id=candidate_id,
                    skill_id=skill.id,
                    proficiency=prof,
                )
                await self.candidate_repo.add_candidate_skill(cs)

        return await self.candidate_repo.get_by_id(candidate_id)

    async def delete_candidate(self, candidate_id: uuid.UUID, organization_id: uuid.UUID) -> None:
        candidate = await self.get_candidate_by_id(candidate_id, organization_id)
        await self.candidate_repo.delete(candidate)

    async def list_candidates(
        self,
        organization_id: uuid.UUID,
        params: PaginationParams,
        status: Optional[CandidateStatus] = None,
        search: Optional[str] = None,
    ) -> Page[Candidate]:
        items, total = await self.candidate_repo.list_candidates(
            organization_id=organization_id,
            skip=params.offset,
            limit=params.limit,
            status=status,
            search=search,
        )
        return Page.create(items=items, total=total, params=params)
