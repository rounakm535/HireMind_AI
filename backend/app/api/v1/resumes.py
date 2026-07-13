import uuid
from typing import List
from fastapi import APIRouter, Depends, Form, UploadFile, File, status
from app.schemas.resume import ResumeResponse, MatchScoreResponse
from app.dependencies.auth import get_resume_service, get_current_user, RoleChecker
from app.services.resume_service import ResumeService
from app.models.user import User, UserRole
from app.exceptions.custom import PermissionDeniedError

router = APIRouter(prefix="/resumes", tags=["Resumes"])

# Read permissions
read_checker = RoleChecker([UserRole.ADMIN, UserRole.RECRUITER, UserRole.HIRING_MANAGER])
# Write permissions (upload/delete/match)
write_checker = RoleChecker([UserRole.ADMIN, UserRole.RECRUITER])


@router.post("/upload", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    candidate_id: uuid.UUID = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(write_checker),
    resume_service: ResumeService = Depends(get_resume_service),
):
    if not current_user.organization_id:
        raise PermissionDeniedError("User must belong to an organization to upload resumes.")
    
    file_content = await file.read()
    return await resume_service.upload_resume(
        candidate_id=candidate_id,
        file_name=file.filename,
        file_content=file_content,
        organization_id=current_user.organization_id,
    )


@router.get("/{id}", response_model=ResumeResponse, status_code=status.HTTP_200_OK)
async def get_resume(
    id: uuid.UUID,
    current_user: User = Depends(read_checker),
    resume_service: ResumeService = Depends(get_resume_service),
):
    if not current_user.organization_id:
        raise PermissionDeniedError("User must belong to an organization.")
    return await resume_service.get_resume(id, current_user.organization_id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    id: uuid.UUID,
    current_user: User = Depends(write_checker),
    resume_service: ResumeService = Depends(get_resume_service),
):
    if not current_user.organization_id:
        raise PermissionDeniedError("User must belong to an organization.")
    await resume_service.delete_resume(id, current_user.organization_id)


@router.post("/match", response_model=MatchScoreResponse, status_code=status.HTTP_200_OK)
async def match_resume_to_job(
    resume_id: uuid.UUID,
    job_id: uuid.UUID,
    current_user: User = Depends(write_checker),
    resume_service: ResumeService = Depends(get_resume_service),
):
    if not current_user.organization_id:
        raise PermissionDeniedError("User must belong to an organization.")
    return await resume_service.screen_and_match(
        resume_id=resume_id,
        job_id=job_id,
        organization_id=current_user.organization_id,
    )


@router.get("/job-rankings/{job_id}", response_model=List[MatchScoreResponse], status_code=status.HTTP_200_OK)
async def get_job_rankings(
    job_id: uuid.UUID,
    current_user: User = Depends(read_checker),
    resume_service: ResumeService = Depends(get_resume_service),
):
    if not current_user.organization_id:
        raise PermissionDeniedError("User must belong to an organization.")
    return await resume_service.get_job_rankings(job_id, current_user.organization_id)
