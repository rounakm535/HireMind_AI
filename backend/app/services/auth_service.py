import uuid
from typing import Optional, Tuple
from app.core.security import get_password_hash, verify_password
from app.core.jwt import create_access_token, create_refresh_token, decode_token
from app.core.config import settings
from app.models.user import User, UserRole, AuditLog
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserRegister, Token
from app.exceptions.custom import InvalidCredentialsError, DuplicateEntityError, EntityNotFoundError, InvalidTokenError


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register(self, schema: UserRegister) -> User:
        # Check if email is already taken
        existing_user = await self.user_repo.get_by_email(schema.email)
        if existing_user:
            raise DuplicateEntityError(f"Email {schema.email} is already registered.")

        # Determine organization_id
        org_id = schema.organization_id
        if not org_id and schema.organization_name:
            # Check if organization already exists
            existing_org = await self.user_repo.get_organization_by_name(schema.organization_name)
            if existing_org:
                org_id = existing_org.id
            else:
                new_org = await self.user_repo.create_organization(schema.organization_name)
                org_id = new_org.id

        # Hash the password
        hashed_password = get_password_hash(schema.password)

        # Create user instance
        user = User(
            email=schema.email,
            hashed_password=hashed_password,
            first_name=schema.first_name,
            last_name=schema.last_name,
            role=schema.role,
            organization_id=org_id,
            is_active=True,
        )

        created_user = await self.user_repo.create(user)

        # Log audit action
        audit = AuditLog(
            user_id=created_user.id,
            action="register",
            entity_type="users",
            entity_id=created_user.id,
            details={"email": created_user.email, "role": created_user.role.value},
        )
        await self.user_repo.create_audit_log(audit)

        return created_user

    async def login(self, email: str, password: str) -> Token:
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()

        if not user.is_active:
            raise InvalidCredentialsError("User account is inactive.")

        # Generate tokens
        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)

        # Log audit action
        audit = AuditLog(
            user_id=user.id,
            action="login",
            entity_type="users",
            entity_id=user.id,
            details={"email": user.email},
        )
        await self.user_repo.create_audit_log(audit)

        return Token(access_token=access_token, refresh_token=refresh_token)

    async def refresh_tokens(self, refresh_token: str) -> Token:
        payload = decode_token(refresh_token, settings.REFRESH_SECRET_KEY)
        if not payload or payload.get("type") != "refresh":
            raise InvalidTokenError("Invalid or expired refresh token.")

        user_id_str = payload.get("sub")
        if not user_id_str:
            raise InvalidTokenError("Token payload is missing user ID.")

        try:
            user_id = uuid.UUID(user_id_str)
        except ValueError:
            raise InvalidTokenError("Invalid user ID in token.")

        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise InvalidTokenError("User associated with this token is not active.")

        # Generate new tokens
        access_token = create_access_token(subject=user.id)
        new_refresh_token = create_refresh_token(subject=user.id)

        return Token(access_token=access_token, refresh_token=new_refresh_token)
