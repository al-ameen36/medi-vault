from typing import Optional
from pydantic import BaseModel
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    dob: str
    role: str
    username: Optional[str] = None


class UserCreateType(UserBase):
    password: str


class UserCreateInput(BaseModel):
    email: str
    password: str
    phone_number: str
    role: str


class UserType(UserBase):
    id: int
