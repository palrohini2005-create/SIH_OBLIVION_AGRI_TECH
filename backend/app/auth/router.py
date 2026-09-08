"""Sign-in, sign-up and the current account.

Authentication is a session cookie the browser sends on every request. Anything
without a valid session answers 401, which the front end reads as "signed out"
and acts on by returning the user to the login screen.
"""

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app import models
from app.auth import service
from app.auth.schemas import AuthResponse, LoginRequest, MeResponse, SignupRequest, UserOut
from app.auth.session import current_user, end_session, start_session, current_admin
from app.common.schemas import SimpleResponse
from app.core.database import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)) -> AuthResponse:
    user = service.sign_in(db, payload.email, payload.password)
    start_session(response, user.email)

    if not user.terms_accepted_current:
        return AuthResponse(user=UserOut.model_validate(user), termsRequired=True)
    return AuthResponse(user=UserOut.model_validate(user))


@router.post("/signup", response_model=AuthResponse)
def signup(payload: SignupRequest, response: Response, db: Session = Depends(get_db)) -> AuthResponse:
    user = service.sign_up(db, payload.email, payload.password, payload.accepted_terms)
    start_session(response, user.email)
    return AuthResponse(user=UserOut.model_validate(user), needsEmailVerification=False)


@router.post("/logout", response_model=SimpleResponse)
def logout(response: Response) -> SimpleResponse:
    end_session(response)
    return SimpleResponse()


@router.get("/me", response_model=MeResponse)
def me(user: models.User = Depends(current_user)) -> MeResponse:
    """Used by the portal's server-rendered pages to choose dashboard or login."""
    return MeResponse(user=UserOut.model_validate(user))

@router.get("/dashboard/admin")
def admin_dashboard(admin: models.User = Depends(current_admin)):
    return {"ok": True, "message": f"Welcome Admin {admin.email}"}

@router.get("/dashboard/user")
def user_dashboard(user: models.User = Depends(current_user)):
    return {"ok": True, "message": f"Welcome User {user.email}"}
