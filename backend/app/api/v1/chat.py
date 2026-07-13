from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from app.dependencies.auth import get_resume_service, get_current_user, RoleChecker
from app.services.resume_service import ResumeService
from app.models.user import User, UserRole
from app.exceptions.custom import PermissionDeniedError

router = APIRouter(prefix="/chat", tags=["Recruiter AI Chat Assistant"])

read_checker = RoleChecker([UserRole.ADMIN, UserRole.RECRUITER, UserRole.HIRING_MANAGER])


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    response: str


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat_assistant(
    request: ChatRequest,
    current_user: User = Depends(read_checker),
    resume_service: ResumeService = Depends(get_resume_service),
):
    if not current_user.organization_id:
        raise PermissionDeniedError("User must belong to an organization.")
    res = await resume_service.chat_helper(request.query, current_user.organization_id)
    return ChatResponse(response=res)
