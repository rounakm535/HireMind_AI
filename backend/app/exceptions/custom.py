from typing import Any, Dict, Optional


class HireMindException(Exception):
    """Base exception for all HireMind AI domain errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code or self.__class__.__name__
        self.details = details or {}


class EntityNotFoundError(HireMindException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=404, code="ENTITY_NOT_FOUND", details=details)


class DuplicateEntityError(HireMindException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=409, code="DUPLICATE_ENTITY", details=details)


class InvalidCredentialsError(HireMindException):
    def __init__(self, message: str = "Invalid email or password", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=401, code="INVALID_CREDENTIALS", details=details)


class PermissionDeniedError(HireMindException):
    def __init__(self, message: str = "Permission denied", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=403, code="PERMISSION_DENIED", details=details)


class TokenExpiredError(HireMindException):
    def __init__(self, message: str = "Token has expired", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=401, code="TOKEN_EXPIRED", details=details)


class InvalidTokenError(HireMindException):
    def __init__(self, message: str = "Invalid token", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=401, code="INVALID_TOKEN", details=details)


class AIServiceError(HireMindException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=502, code="AI_SERVICE_ERROR", details=details)


class FileStorageError(HireMindException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=500, code="FILE_STORAGE_ERROR", details=details)
