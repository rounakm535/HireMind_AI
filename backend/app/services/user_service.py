import uuid
from typing import List, Optional
from app.core.security import get_password_hash
from app.models.user import User, AuditLog
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserUpdate
from app.exceptions.custom import EntityNotFoundError


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_user_by_id(self, user_id: uuid.UUID) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise EntityNotFoundError(f"User with ID {user_id} not found.")
        return user

    async def update_user(self, user_id: uuid.UUID, schema: UserUpdate) -> User:
        user = await self.get_user_by_id(user_id)

        update_data = schema.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        for key, value in update_data.items():
            setattr(user, key, value)

        updated_user = await self.user_repo.update(user)

        # Log audit action
        audit = AuditLog(
            user_id=user.id,
            action="update_user",
            entity_type="users",
            entity_id=user.id,
            details={"updated_fields": list(update_data.keys())},
        )
        await self.user_repo.create_audit_log(audit)

        return updated_user

    async def get_audit_logs(self, limit: int = 100) -> List[AuditLog]:
        return await self.user_repo.get_audit_logs(limit)
