from fastapi import APIRouter, Depends, status
from app.schemas.auth import UserRegister, LoginRequest, RefreshTokenRequest, Token
from app.schemas.user import UserResponse
from app.dependencies.auth import get_auth_service, get_current_user
from app.services.auth_service import AuthService
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    schema: UserRegister,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.register(schema)


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(
    schema: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.login(schema.email, schema.password)


@router.post("/refresh", response_model=Token, status_code=status.HTTP_200_OK)
async def refresh(
    schema: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.refresh_tokens(schema.refresh_token)


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
