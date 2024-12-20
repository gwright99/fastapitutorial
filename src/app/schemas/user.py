from typing import Optional

from pydantic import BaseModel, EmailStr, Field

__all__ = ["UserCreate", "UserUpdate", "User", "ShowUser"]


class UserBase(BaseModel):
    full_name: Optional[str] = None
    email: EmailStr
    is_superuser: bool = False
    password: str = Field(..., min_length=4)


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr


# Properties to receive via API on update
class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: Optional[int] = None

    # class Config:
    #   orm_mode = True
    model_config = {"from_attributes": True}


# Additional properties to return via API
class User(UserInDBBase):
    pass


class ShowUser(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    # Tell Pydantic to convert even non-dict obj to JSON
    # class Config:
    #   orm_mode = True
    model_config = {"from_attributes": True}


class UserCreate201(BaseModel):
    message: str
