import re

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


class APIException(HTTPException):
    """Base custom API exception"""

    def __init__(
        self, status_code: int, message: str, headers: dict | None = None,
    ):
        super().__init__(
            status_code=status_code, detail=message, headers=headers,
        )
        self.message = message


class BadRequest_400(APIException):
    """400: Bad Request"""

    def __init__(self, message: str = "Bad request"):
        super().__init__(400, message)


class Unauthorized_401(APIException):
    """401: Unauthorized"""

    def __init__(
        self,
        message: str = "Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    ):
        super().__init__(401, message, headers)


class Forbidden_403(APIException):
    """403: Forbidden"""

    def __init__(self, message: str = "Forbidden"):
        super().__init__(403, message)


class NotFound_404(APIException):
    """404: Not Found"""

    def __init__(self, message: str = "Resource(s) not found"):
        super().__init__(404, message)


class Conflict_409(APIException):
    """409: Conflict (e.g. resource already exists)"""

    def __init__(self, exception: IntegrityError | None = None):
        if exception is not None:
            match = re.search(r"Key \((.*?)\)=", str(exception.orig))
            key = match.group(1) if match else "unknown"
            message = f"This {key} is already taken!"
        else:
            key = "unknown"
            message = "Resource conflict occurred"

        super().__init__(409, message)
        self.key = key


class UnprocessableEntity_422(APIException):
    """422: Unprocessable Entity"""

    def __init__(self, message: str = "Unprocessable entity"):
        super().__init__(422, message)

