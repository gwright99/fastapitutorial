from pydantic import BaseModel, EmailStr, Field


# properties required during user creation
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=4)


class ShowUser(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    # Tell Pydantic to convert even non-dict obj to JSON
    class Config:
        orm_mode = True
