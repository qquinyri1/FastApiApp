from datetime import date
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class ContactModel(BaseModel):
    name: str = Field(max_length=25)
    surname: Optional[str]
    email: Optional[EmailStr] = "example@example.com"
    phone_number: Optional[str]
    birthday: Optional[date]
    extra_info: Optional[str]


class UpdateContactDate(BaseModel):
    day: int = Field(ge=1, le=31)  
    month: int = Field(ge=1, le=12)  
    year: int = Field(ge=1, le=9000)


class ContactResponse(ContactModel):
    id: int

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RequestEmail(BaseModel):
    email: EmailStr