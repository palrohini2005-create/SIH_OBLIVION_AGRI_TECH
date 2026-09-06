from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi import Response
from app import models
from app.common.errors import bad_request, forbidden
from app.auth.session import end_session
from app.core.security import hash_password, verify_password

MINIMUM_PASSWORD_LENGTH = 8


def _account(db: Session) -> models.User:
    """The single row in ``users``."""
    user = db.scalar(select(models.User).limit(1))
    if user is None:
        raise RuntimeError("The database has no account. Run: python -m scripts.reset_db")
    return user


def sign_in(db: Session, email: str, password: str) -> models.User:
    email = (email or "").strip()
    password = password or ""

    if "@" not in email:
        raise bad_request("Enter a valid email address.")
    if len(password) < MINIMUM_PASSWORD_LENGTH:
        raise bad_request(
            f"Password must be at least {MINIMUM_PASSWORD_LENGTH} characters. "
            "In this build any password of that length works."
        )

    user= db.query(models.User).filter(models.User.email == email.lower()).first
    if not user:
        raise forbidden('Invalid credentials')

    if not verify_password(password, user.hashed_password):
        raise forbidden("Invalid credentials")
    
    return user


def sign_up(db: Session, email: str, password: str, accepted_terms: bool) -> models.User:
    """The real portal emails a verification link. Here the account signs in."""
    if not accepted_terms:
        raise bad_request("Please accept the Terms and Privacy Policy to create an account.")

    existing = db.query(models.User).filter(models.User.email == email).first()
    if existing:
        raise bad_request("Account already exists with this email.")
    
    hashed_pw=hash_password(password)

    user = models.User(
        email=email,
        hashed_password = hashed_pw,
        accepted_terms=accepted_terms,
        role='user'
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def sign_out(response: Response) -> dict:
    """Clear the session cookie and sign the user out."""
    end_session(response)
    return {"ok": True, "message": "Signed out successfully"}
