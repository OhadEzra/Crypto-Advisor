from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional


class SignupRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    is_onboarded: bool
    name: str


class PreferenceRequest(BaseModel):
    assets: List[str]
    investor_type: str
    content_types: List[str]


class PreferenceResponse(PreferenceRequest):
    pass


class VoteRequest(BaseModel):
    section: str
    item_id: str
    vote: int = Field(ge=-1, le=1)


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_onboarded: bool
    preferences: Optional[PreferenceResponse] = None
