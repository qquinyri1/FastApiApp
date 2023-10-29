from datetime import date
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class Contactt(BaseModel):
    name: str = Field(max_length=100)
    surname: Optional[str]
    email: Optional[EmailStr] = "example@example.com"
    phone_number: Optional[str]
    birthday: Optional[date]
    extra_info: Optional[str]


class Update(BaseModel):
    day: int = Field(ge=1, le=31)  
    month: int = Field(ge=1, le=12)  
    year: int = Field(ge=1, le=9000)


class ContactResponse(Contactt):
    id: int

    class Config:
        orm_mode = True


class Userr(BaseModel):
    username: str = Field(min_length=2, max_length=16)
    email: str
    password: str = Field(min_length=8, max_length=30)


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


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"