import re

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


class APIException(HTTPException):
    """Base custom API exception."""

    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: dict | None = None,
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headers,
        )

    def get_response_body(self, not_default_detail: str | None = None):
        return {"detail": self.detail}


class OK200(APIException):
    """200: OK."""

    def __init__(self, detail: str = "OK") -> None:
        super().__init__(200, detail)


class Created201(APIException):
    """201: Created."""

    def __init__(self, detail: str = "Created") -> None:
        super().__init__(201, detail)


class BadRequest400(APIException):
    """400: Bad Request."""

    def __init__(self, detail: str = "Bad request") -> None:
        super().__init__(400, detail)


class Unauthorized401(APIException):
    """401: Unauthorized."""

    def __init__(
        self,
        detail: str = "Unauthorized",
        headers: dict | None = None,
    ) -> None:
        if headers is None:
            headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(401, detail, headers)


class Forbidden403(APIException):
    """403: Forbidden."""

    def __init__(self, detail: str = "Forbidden") -> None:
        super().__init__(403, detail)


class NotFound404(APIException):
    """404: Not Found."""

    def __init__(self, detail: str = "Resource(s) not found") -> None:
        super().__init__(404, detail)


class Conflict409(APIException):
    """409: Conflict (e.g. resource already exists)."""

    def __init__(self, exception: IntegrityError | None = None) -> None:
        if exception is not None:
            match = re.search(r"Key \((.*?)\)=", str(exception.orig))
            key = match.group(1) if match else "unknown"
            detail = f"This {key} is already taken!"
        else:
            key = "unknown"
            detail = "Resource conflict occurred"

        super().__init__(409, detail)
        self.key = key


class UnprocessableEntity422(APIException):
    """422: Unprocessable Entity."""

    def __init__(self, detail: str = "Unprocessable entity") -> None:
        super().__init__(422, detail)


# responses={
#    200: http_exceptions.OK200().get_response_body(),
#    201: http_exceptions.Created201().get_response_body(),
#    400: http_exceptions.BadRequest400().get_response_body(),
#    401: http_exceptions.Unauthorized401().get_response_body(),
#    403: http_exceptions.Forbidden403().get_response_body(),
#    404: http_exceptions.NotFound404().get_response_body(),
#    409: http_exceptions.Conflict409().get_response_body(),
#    422: http_exceptions.UnprocessableEntity422().get_response_body(),
# },
