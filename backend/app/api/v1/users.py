from fastapi import APIRouter, Depends, status
from typing import List
from app.schemas.user import UserResponse, UserUpdate
from app.dependencies.auth import get_user_service, get_current_user, RoleChecker
from app.services.user_service import UserService
from app.models.user import User, UserRole

router = APIRouter(prefix="/users", tags=["Users"])


@router.put("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_me(
    schema: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.update_user(current_user.id, schema)


@router.get(
    "/audit-logs",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(RoleChecker([UserRole.ADMIN]))],
)
async def get_audit_logs(
    limit: int = 100,
    user_service: UserService = Depends(get_user_service),
):
    # Retrieve system audit logs for administrative view
    logs = await user_service.get_audit_logs(limit)
    return [
        {
            "id": log.id,
            "user_id": log.user_id,
            "action": log.action,
            "entity_type": log.entity_type,
            "entity_id": log.entity_id,
            "details": log.details,
            "ip_address": log.ip_address,
            "created_at": log.created_at,
        }
        for log in logs
    ]
