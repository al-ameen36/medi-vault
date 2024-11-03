import datetime
from pydantic import BaseModel
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    dob: str
    role: str


class UserCreateType(UserBase):
    password: str


class UserType(UserBase):
    id: int
