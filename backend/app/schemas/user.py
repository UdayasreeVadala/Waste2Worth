from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    business_type: str | None = None
    country: str | None = "India"
    location: str | None = None
    phone: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    business_type: str | None = None
    country: str | None = None
    location: str | None = None
    phone: str | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse