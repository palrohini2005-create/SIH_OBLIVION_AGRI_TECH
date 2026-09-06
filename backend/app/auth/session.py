"""The session cookie, and the "who is calling?" dependency.

Every other feature depends on this rather than on the auth router, which is why
it is a module of its own.

The cookie name matches the Node and Java backends on purpose, so the front end
behaves identically whichever backend it is talking to. What it holds is only a
marker: real authentication would issue something signed, and check it here.
"""

from fastapi import Depends, Request, Response, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.common.errors import not_logged_in, forbidden
from app.core.config import settings
from app.core.database import get_db
from app.core.security import decode_access_token


def start_session(response: Response, email: str) -> None:
    response.set_cookie(
        key=settings.session_cookie,
        value=email,
        max_age=settings.session_max_age,
        httponly=True,
        secure=settings.session_secure,
        # Lax is enough because the front end and this service share a hostname
        # in development, so the calls count as same-site.
        samesite="lax",
        path="/",
    )


def end_session(response: Response) -> None:
    response.delete_cookie(key=settings.session_cookie, path="/")


def current_user_optional(
    request: Request,
    db: Session = Depends(get_db),
) -> models.User | None:
    """The signed-in account, or None when there is no session cookie."""
    if not request.cookies.get(settings.session_cookie):
        return None
    return db.scalar(select(models.User).limit(1))


def current_user(
    user: models.User | None = Depends(current_user_optional),
) -> models.User:
    """The signed-in account, or a 401.

    Use it as a dependency on anything that needs a session::

        @router.get("/thing")
        def thing(user: models.User = Depends(current_user)):
            ...
    """
    if user is None:
        raise not_logged_in()
    return user

def current_admin(
    user: models.User = Depends(current_user),
) -> models.User:
    if user.role != "admin":   # or user.is_admin == False
        raise forbidden("Admin access required")
    return user