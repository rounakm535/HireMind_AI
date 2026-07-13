import uuid
from typing import Optional
from fastapi import APIRouter, Depends, status, Query
from app.schemas.job import JobCreate, JobUpdate, JobResponse
from app.utils.pagination import PaginationParams, Page
from app.dependencies.auth import get_job_service, get_current_user, RoleChecker
from app.services.job_service import JobService
from app.models.user import User, UserRole
from app.models.job import JobStatus, JobType
from app.exceptions.custom import PermissionDeniedError

router = APIRouter(prefix="/jobs", tags=["Jobs"])

# Read permissions for recruiters, hiring managers, and admins
read_checker = RoleChecker([UserRole.ADMIN, UserRole.RECRUITER, UserRole.HIRING_MANAGER])
# Write permissions for recruiters and admins
write_checker = RoleChecker([UserRole.ADMIN, UserRole.RECRUITER])


@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    schema: JobCreate,
    current_user: User = Depends(write_checker),
    job_service: JobService = Depends(get_job_service),
):
    if not current_user.organization_id:
        raise PermissionDeniedError("User must belong to an organization to create jobs.")
    return await job_service.create_job(schema, current_user.organization_id)


@router.get("/", response_model=Page[JobResponse], status_code=status.HTTP_200_OK)
async def list_jobs(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    job_type: Optional[JobType] = None,
    status: Optional[JobStatus] = None,
    search: Optional[str] = None,
    current_user: User = Depends(read_checker),
    job_service: JobService = Depends(get_job_service),
):
    if not current_user.organization_id:
        raise PermissionDeniedError("User must belong to an organization to view jobs.")
    params = PaginationParams(page=page, size=size)
    return await job_service.list_jobs(
        organization_id=current_user.organization_id,
        params=params,
        job_type=job_type,
        status=status,
        search=search,
    )


@router.get("/{id}", response_model=JobResponse, status_code=status.HTTP_200_OK)
async def get_job(
    id: uuid.UUID,
    current_user: User = Depends(read_checker),
    job_service: JobService = Depends(get_job_service),
):
    if not current_user.organization_id:
        raise PermissionDeniedError("User must belong to an organization to view jobs.")
    return await job_service.get_job_by_id(id, current_user.organization_id)


@router.put("/{id}", response_model=JobResponse, status_code=status.HTTP_200_OK)
async def update_job(
    id: uuid.UUID,
    schema: JobUpdate,
    current_user: User = Depends(write_checker),
    job_service: JobService = Depends(get_job_service),
):
    if not current_user.organization_id:
        raise PermissionDeniedError("User must belong to an organization to edit jobs.")
    return await job_service.update_job(id, schema, current_user.organization_id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    id: uuid.UUID,
    current_user: User = Depends(write_checker),
    job_service: JobService = Depends(get_job_service),
):
    if not current_user.organization_id:
        raise PermissionDeniedError("User must belong to an organization to delete jobs.")
    await job_service.delete_job(id, current_user.organization_id)
