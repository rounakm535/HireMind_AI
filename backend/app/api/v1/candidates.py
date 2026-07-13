import uuid
from typing import Optional
from fastapi import APIRouter, Depends, status, Query
from app.schemas.candidate import CandidateCreate, CandidateUpdate, CandidateResponse
from app.utils.pagination import PaginationParams, Page
from app.dependencies.auth import get_candidate_service, get_current_user, RoleChecker
from app.services.candidate_service import CandidateService
from app.models.user import User, UserRole
from app.models.candidate import CandidateStatus
from app.exceptions.custom import PermissionDeniedError

router = APIRouter(prefix="/candidates", tags=["Candidates"])

# Read permissions for recruiters, hiring managers, and admins
read_checker = RoleChecker([UserRole.ADMIN, UserRole.RECRUITER, UserRole.HIRING_MANAGER])
# Write permissions for recruiters and admins
write_checker = RoleChecker([UserRole.ADMIN, UserRole.RECRUITER])


@router.post("/", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED)
async def create_candidate(
    schema: CandidateCreate,
    current_user: User = Depends(write_checker),
    candidate_service: CandidateService = Depends(get_candidate_service),
):
    if not current_user.organization_id:
        raise PermissionDeniedError("User must belong to an organization to create candidates.")
    return await candidate_service.create_candidate(schema, current_user.organization_id)


@router.get("/", response_model=Page[CandidateResponse], status_code=status.HTTP_200_OK)
async def list_candidates(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    status: Optional[CandidateStatus] = None,
    search: Optional[str] = None,
    current_user: User = Depends(read_checker),
    candidate_service: CandidateService = Depends(get_candidate_service),
):
    if not current_user.organization_id:
        raise PermissionDeniedError("User must belong to an organization to view candidates.")
    params = PaginationParams(page=page, size=size)
    return await candidate_service.list_candidates(
        organization_id=current_user.organization_id,
        params=params,
        status=status,
        search=search,
    )


@router.get("/{id}", response_model=CandidateResponse, status_code=status.HTTP_200_OK)
async def get_candidate(
    id: uuid.UUID,
    current_user: User = Depends(read_checker),
    candidate_service: CandidateService = Depends(get_candidate_service),
):
    if not current_user.organization_id:
        raise PermissionDeniedError("User must belong to an organization to view candidates.")
    return await candidate_service.get_candidate_by_id(id, current_user.organization_id)


@router.put("/{id}", response_model=CandidateResponse, status_code=status.HTTP_200_OK)
async def update_candidate(
    id: uuid.UUID,
    schema: CandidateUpdate,
    current_user: User = Depends(write_checker),
    candidate_service: CandidateService = Depends(get_candidate_service),
):
    if not current_user.organization_id:
        raise PermissionDeniedError("User must belong to an organization to edit candidates.")
    return await candidate_service.update_candidate(id, schema, current_user.organization_id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate(
    id: uuid.UUID,
    current_user: User = Depends(write_checker),
    candidate_service: CandidateService = Depends(get_candidate_service),
):
    if not current_user.organization_id:
        raise PermissionDeniedError("User must belong to an organization to delete candidates.")
    await candidate_service.delete_candidate(id, current_user.organization_id)
