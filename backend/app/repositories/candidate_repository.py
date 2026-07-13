import uuid
from typing import List, Optional, Tuple
from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.candidate import Candidate, CandidateStatus, CandidateSkill
from app.models.skill import Skill


class CandidateRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, candidate_id: uuid.UUID) -> Optional[Candidate]:
        result = await self.db.execute(
            select(Candidate)
            .options(
                selectinload(Candidate.candidate_skills).selectinload(CandidateSkill.skill)
            )
            .where(Candidate.id == candidate_id)
        )
        return result.scalars().first()

    async def create(self, candidate: Candidate) -> Candidate:
        self.db.add(candidate)
        await self.db.flush()
        return candidate

    async def update(self, candidate: Candidate) -> Candidate:
        self.db.add(candidate)
        await self.db.flush()
        return candidate

    async def delete(self, candidate: Candidate) -> None:
        await self.db.delete(candidate)
        await self.db.flush()

    async def list_candidates(
        self,
        organization_id: uuid.UUID,
        skip: int = 0,
        limit: int = 20,
        status: Optional[CandidateStatus] = None,
        search: Optional[str] = None,
    ) -> Tuple[List[Candidate], int]:
        # Build query
        query = select(Candidate).where(Candidate.organization_id == organization_id)

        if status:
            query = query.where(Candidate.status == status)
        if search:
            query = query.where(
                or_(
                    Candidate.first_name.ilike(f"%{search}%"),
                    Candidate.last_name.ilike(f"%{search}%"),
                    Candidate.email.ilike(f"%{search}%"),
                )
            )

        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar_one()

        # Retrieve items with relationships preloaded
        query = (
            query.options(
                selectinload(Candidate.candidate_skills).selectinload(CandidateSkill.skill)
            )
            .order_by(Candidate.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        items_result = await self.db.execute(query)
        items = list(items_result.scalars().all())

        return items, total

    async def get_skill_by_name(self, name: str) -> Optional[Skill]:
        result = await self.db.execute(select(Skill).where(Skill.name == name))
        return result.scalars().first()

    async def create_skill(self, name: str) -> Skill:
        skill = Skill(name=name)
        self.db.add(skill)
        await self.db.flush()
        return skill

    async def add_candidate_skill(self, candidate_skill: CandidateSkill) -> CandidateSkill:
        self.db.add(candidate_skill)
        await self.db.flush()
        return candidate_skill

    async def clear_candidate_skills(self, candidate_id: uuid.UUID) -> None:
        result = await self.db.execute(
            select(CandidateSkill).where(CandidateSkill.candidate_id == candidate_id)
        )
        for cs in result.scalars().all():
            await self.db.delete(cs)
        await self.db.flush()
