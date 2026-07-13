import uuid
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from app.schemas.resume import EmailLogResponse
from app.dependencies.auth import get_resume_service, get_current_user, RoleChecker
from app.services.resume_service import ResumeService
from app.models.user import User, UserRole
from app.exceptions.custom import PermissionDeniedError

router = APIRouter(prefix="/emails", tags=["Emails"])

write_checker = RoleChecker([UserRole.ADMIN, UserRole.RECRUITER])


class EmailGenerateRequest(BaseModel):
    candidate_id: uuid.UUID
    job_id: uuid.UUID
    template_type: str  # interview_invitation, shortlist, rejection, etc.


@router.post("/generate", response_model=EmailLogResponse, status_code=status.HTTP_201_CREATED)
async def generate_email(
    request: EmailGenerateRequest,
    current_user: User = Depends(write_checker),
    resume_service: ResumeService = Depends(get_resume_service),
):
    if not current_user.organization_id:
        raise PermissionDeniedError("User must belong to an organization.")
    return await resume_service.generate_candidate_email(
        candidate_id=request.candidate_id,
        job_id=request.job_id,
        template_type=request.template_type,
        sender_id=current_user.id,
        organization_id=current_user.organization_id,
    )
