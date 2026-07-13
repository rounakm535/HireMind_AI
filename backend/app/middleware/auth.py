import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.jwt import decode_token
from app.core.config import settings


class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Extract JWT from Authorization Header
        auth_header = request.headers.get("Authorization")
        request.state.user_id = None
        
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            payload = decode_token(token, settings.SECRET_KEY)
            if payload and payload.get("type") == "access":
                sub = payload.get("sub")
                try:
                    request.state.user_id = uuid.UUID(sub) if sub else None
                except ValueError:
                    pass

        response = await call_next(request)
        return response
