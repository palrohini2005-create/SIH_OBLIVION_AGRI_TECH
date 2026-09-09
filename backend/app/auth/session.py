"""The session cookie, and the "who is calling?" dependency.

Every other feature depends on this rather than on the auth router, which is why
it is a module of its own.

The cookie name matches the Node and Java backends on purpose, so the front end
behaves identically whichever backend it is talking to. What it holds is only a
marker: real authentication would issue something signed, and check it here.
"""

from fastapi import Depends, Request, Response, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.common.errors import not_logged_in, forbidden
from app.core.config import settings
from app.core.database import get_db
from app.core.security import decode_access_token, create_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

def start_session(response: Response, email: str) -> None:
    token = create_access_token(data={"sub": email})
    response.set_cookie(
        key=settings.session_cookie,
        value=email,
        max_age=settings.session_max_age,
        httponly=True,
        secure=settings.session_secure,
        samesite="lax",
        path="/",
    )


def end_session(response: Response) -> None:
    response.delete_cookie(key=settings.session_cookie, path="/")


def current_user_optional(
    request: Request,
    token_from_header: str | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> models.User | None:
    token = request.cookies.get(settings.session_cookie) or token_from_header
    if not token:
        return None
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if not email:
            return None

        user = db.scalar(select(models.User).where(models.User.email == email))
        return user
    except ValueError:
        return None

def current_user(
    user: models.User | None = Depends(current_user_optional),
) -> models.User:
    
    if user is None:
        raise not_logged_in()
    return user

def current_admin(
    user: models.User = Depends(current_user),
) -> models.User:
    if getattr(user, "role", None) != "admin" and not getattr(
        user, "is_admin", False
    ):
        raise forbidden("Admin access required")
    return user