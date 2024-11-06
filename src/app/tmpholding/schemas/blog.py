from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator


class CreateBlog(BaseModel):
    title: str
    slug: str
    content: Optional[str] = None

    # @pydantic.root_validator(pre=True)   # This function before executing Pydantic validation (since it generates
    # one of the required fields). Replace by `model_validator` in Pydantic v2.
    @model_validator(mode="before")
    def generate_slug(cls, values):
        if "title" in values:
            values["slug"] = values.get("title").replace(" ", "-").lower()
        return values


class ShowBlog(BaseModel):
    title: str
    content: Optional[str]
    # created_at: date
    created_at: datetime

    # class Config:
    #   orm_mode = True
    model_config = {"from_attributes": True}


class UpdateBlog(CreateBlog):  # < Note intheritance from CreateBlog Class
    pass
