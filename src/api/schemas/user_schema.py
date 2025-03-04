from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr = Field(..., min_length=1, max_length=254)
    name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=10)
    tenant_id: int
    is_admin: bool = False


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None


class PasswordChange(BaseModel):
    current_password: str = Field(..., min_length=8, max_length=10)
    new_password: str = Field(..., min_length=8, max_length=10)


class EmailVerification(BaseModel):
    email_code: str


class UserResponse(UserBase):
    id: int
    tenant_id: int
    is_admin: bool
    email_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
