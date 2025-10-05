from fastapi import HTTPException, status


class PandacPOSException(Exception):
    """Base exception for Pandac POS application."""
    pass


class AuthenticationException(PandacPOSException):
    """Exception raised for authentication errors."""
    pass


class AuthorizationException(PandacPOSException):
    """Exception raised for authorization errors."""
    pass


class ValidationException(PandacPOSException):
    """Exception raised for validation errors."""
    pass


class NotFoundException(PandacPOSException):
    """Exception raised when a resource is not found."""
    pass


class DuplicateException(PandacPOSException):
    """Exception raised when trying to create a duplicate resource."""
    pass


class BusinessLogicException(PandacPOSException):
    """Exception raised for business logic violations."""
    pass


# HTTP Exceptions
class HTTPUnauthorized(HTTPException):
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class HTTPForbidden(HTTPException):
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class HTTPNotFound(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class HTTPBadRequest(HTTPException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class HTTPConflict(HTTPException):
    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )
