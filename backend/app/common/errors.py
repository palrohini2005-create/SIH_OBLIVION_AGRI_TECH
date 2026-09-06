"""Failures, in the shape the front end expects.

The API contract treats an HTTP 4xx and an ``{"ok": false}`` body as equally
valid ways to fail, and 401 or 403 specifically as "the session is gone", which
the front end acts on by returning the user to the login screen.
"""

from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class ApiError(Exception):
    """Raise this anywhere; the handler below turns it into the right JSON."""

    def __init__(
        self,
        status_code: int,
        message: str,
        user_message: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.message = message
        self.user_message = user_message


def bad_request(message: str) -> ApiError:
    return ApiError(status.HTTP_400_BAD_REQUEST, message)


def not_logged_in() -> ApiError:
    return ApiError(status.HTTP_401_UNAUTHORIZED, "Not logged in.")


def not_found(message: str) -> ApiError:
    return ApiError(status.HTTP_404_NOT_FOUND, message)

def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApiError)
    async def _api_error(_request: Request, error: ApiError) -> JSONResponse:
        body: dict[str, Any] = {"ok": False, "message": error.message}
        if error.user_message:
            body["userMessage"] = error.user_message
        return JSONResponse(status_code=error.status_code, content=body)

    @app.exception_handler(RequestValidationError)
    async def _validation_error(_request: Request, error: RequestValidationError) -> JSONResponse:
        # FastAPI answers 422 by default. The front end only understands the
        # contract's failure shape, so translate it into that.
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"ok": False, "message": "That request was not valid.", "detail": error.errors()},
        )

    @app.exception_handler(StarletteHTTPException)
    async def _http_error(request: Request, error: StarletteHTTPException) -> JSONResponse:
        """Reshape framework errors, and explain the ones this build causes.

        This backend implements only part of the contract, so an unwritten
        endpoint shows up as a plain 404. Saying so beats "Not Found" appearing
        in the portal with no clue where it came from.
        """
        message = str(error.detail)
        if error.status_code == status.HTTP_404_NOT_FOUND and request.url.path.startswith("/api/"):
            message = (
                f"{request.method} {request.url.path} is not implemented in this backend yet. "
                "See the table in python_backend/README.md."
            )

        return JSONResponse(
            status_code=error.status_code,
            content={"ok": False, "message": message},
            headers=getattr(error, "headers", None),
        )
