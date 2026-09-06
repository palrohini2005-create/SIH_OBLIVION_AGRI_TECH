from pydantic import BaseModel
from app.common.schemas import ApiModel

class UserOut(ApiModel):
    """The signed-in account, as the front end reads it."""
    id: str
    email: str
    role: str = "user"   # <-- add role field
    email_verified: bool = False
    has_password: bool = True
    phone_e164: str | None = None
    phone_verified: bool = False
    status: str = "active"
    terms_accepted_current: bool = False

class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    email: str
    password: str
    accepted_terms: bool = False
    referral_email: str | None = None
    role: str = "user"   # <-- allow admin/user distinction

class AuthResponse(ApiModel):
    ok: bool = True
    user: UserOut
    termsRequired: bool | None = None
    needsEmailVerification: bool | None = None

class MeResponse(ApiModel):
    ok: bool = True
    user: UserOut
