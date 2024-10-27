# fastapi.exceptions.ResponseValidationError: 1 validation errors:
#   {'type': 'date_from_datetime_inexact', 'loc': ('response', 'created_at'), 'msg': 'Datetimes provided to dates should have zero time - e.g. be exact dates', 'input': datetime.datetime(2024, 10, 27, 9, 16, 40, 292227)}
# from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import (  # root_validator < Pydantic v1; replaced by model_validator
    BaseModel,
    model_validator,
)


class CreateBlog(BaseModel):
    title: str
    slug: str
    content: Optional[str] = None

    # @root_validator(pre=True)   # Run this function before executing Pydantic validation (since it generates
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

    class Config:
        orm_mode = True
