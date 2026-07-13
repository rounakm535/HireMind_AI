from fastapi import APIRouter, Depends, status
from app.dependencies.auth import get_resume_service, get_current_user, RoleChecker
from app.services.resume_service import ResumeService
from app.models.user import User, UserRole
from app.exceptions.custom import PermissionDeniedError

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

# Accessible by all roles
read_checker = RoleChecker([UserRole.ADMIN, UserRole.RECRUITER, UserRole.HIRING_MANAGER])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_dashboard(
    current_user: User = Depends(read_checker),
    resume_service: ResumeService = Depends(get_resume_service),
):
    if not current_user.organization_id:
        raise PermissionDeniedError("User must belong to an organization.")
    return await resume_service.get_dashboard_summary(current_user.organization_id)
