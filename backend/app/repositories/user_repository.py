import uuid
from typing import Optional, List
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, AuditLog
from app.models.organization import Organization


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()
        return user

    async def update(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()
        return user

    async def get_organization_by_id(self, org_id: uuid.UUID) -> Optional[Organization]:
        result = await self.db.execute(select(Organization).where(Organization.id == org_id))
        return result.scalars().first()

    async def get_organization_by_name(self, name: str) -> Optional[Organization]:
        result = await self.db.execute(select(Organization).where(Organization.name == name))
        return result.scalars().first()

    async def create_organization(self, name: str) -> Organization:
        org = Organization(name=name)
        self.db.add(org)
        await self.db.flush()
        return org

    async def create_audit_log(self, audit_log: AuditLog) -> AuditLog:
        self.db.add(audit_log)
        await self.db.flush()
        return audit_log

    async def get_audit_logs(self, limit: int = 100) -> List[AuditLog]:
        result = await self.db.execute(
            select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())
