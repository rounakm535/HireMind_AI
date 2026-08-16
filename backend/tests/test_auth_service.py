import pytest
import uuid
from app.db.database import AsyncSessionLocal, init_db
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.schemas.auth import UserRegister
from app.models.user import UserRole
from app.exceptions.custom import InvalidCredentialsError, DuplicateEntityError


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    import asyncio
    asyncio.run(init_db())


@pytest.mark.asyncio
async def test_auth_registration_and_login_flow():
    async with AsyncSessionLocal() as session:
        user_repo = UserRepository(session)
        auth_service = AuthService(user_repo)

        unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        reg_schema = UserRegister(
            email=unique_email,
            password="SecurePassword123!",
            first_name="Test",
            last_name="User",
            role=UserRole.RECRUITER,
            organization_name="HireMind Test Corp",
        )

        user = await auth_service.register(reg_schema)
        assert user.id is not None
        assert user.email == unique_email
        assert user.organization_id is not None

        # Test duplicate registration error
        with pytest.raises(DuplicateEntityError):
            await auth_service.register(reg_schema)

        # Test successful login
        tokens = await auth_service.login(unique_email, "SecurePassword123!")
        assert tokens.access_token is not None
        assert tokens.refresh_token is not None

        # Test invalid password login
        with pytest.raises(InvalidCredentialsError):
            await auth_service.login(unique_email, "WrongPassword!")

        # Test refresh token
        new_tokens = await auth_service.refresh_tokens(tokens.refresh_token)
        assert new_tokens.access_token is not None
