from datetime import date
from pydantic import BaseModel, Field, EmailStr
from typing import Optional


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