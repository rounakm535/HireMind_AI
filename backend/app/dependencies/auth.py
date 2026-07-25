import uuid
from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
from app.core.jwt import decode_token
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.repositories.job_repository import JobRepository
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.resume_repository import ResumeRepository
from app.dependencies.database import (
    get_user_repository,
    get_job_repository,
    get_candidate_repository,
    get_resume_repository,
)
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.job_service import JobService
from app.services.candidate_service import CandidateService
from app.services.resume_service import ResumeService
from app.ai.clients.gemini import GeminiClient
from app.exceptions.custom import InvalidTokenError, PermissionDeniedError, EntityNotFoundError

# HTTP Bearer token extractor
security_scheme = HTTPBearer(auto_error=False)
gemini_instance = GeminiClient()


async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme), user_repo: UserRepository = Depends(get_user_repository)) -> User:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    payload = decode_token(token, settings.SECRET_KEY)
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    sub = payload.get("sub")
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload is invalid.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = uuid.UUID(sub)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive.",
        )

    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in self.allowed_roles:
            raise PermissionDeniedError(
                message=f"Role '{current_user.role.value}' does not have permission to perform this action."
            )
        return current_user


# Service Providers Dependency Injection
def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repo)


def get_user_service(user_repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repo)


def get_job_service(job_repo: JobRepository = Depends(get_job_repository)) -> JobService:
    return JobService(job_repo)


def get_candidate_service(
    candidate_repo: CandidateRepository = Depends(get_candidate_repository),
) -> CandidateService:
    return CandidateService(candidate_repo)


def get_resume_service(
    resume_repo: ResumeRepository = Depends(get_resume_repository),
    candidate_repo: CandidateRepository = Depends(get_candidate_repository),
    job_repo: JobRepository = Depends(get_job_repository),
) -> ResumeService:
    return ResumeService(resume_repo, candidate_repo, job_repo, gemini_instance)
