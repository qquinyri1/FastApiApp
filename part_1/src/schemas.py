from datetime import datetime, date
from pydantic import BaseModel, EmailStr, Field


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: date
    additional_data: str = None


class ContactResponse(ContactBase):
    id: int = 1
    first_name: str = "Dow"
    last_name: str = "John"
    email: str = "example@test.com"
    phone_number: str = "5551234567"
    birthday: date = date(year=1999, month=10, day=5)
    additional_data: str = "Created first contact for test"

    class Config:
        from_attribute = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    avatar: str

    class Config:
        from_attribute = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr