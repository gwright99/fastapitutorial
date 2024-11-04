from typing import Sequence

from pydantic import BaseModel, HttpUrl


class RecipeBase(BaseModel):
    label: str
    source: str
    url: HttpUrl


class RecipeCreate(RecipeBase):
    label: str
    source: str
    url: HttpUrl
    submitter_id: int


class RecipeUpdate(RecipeBase):
    label: str


# Properties shared by models stored in DB
# Why make the distinction between a Recipe and RecipeInDB? This allows us in future to
# # separate fields which are only relevant for the DB, or which we don’t want to return
# to the client (such as a password field).
class RecipeInDBBase(RecipeBase):
    id: int
    submitter_id: int

    # tell the Pydantic model to read the data even if it is not a dict,
    # but an ORM model (or any other arbitrary object with attributes).
    # Without orm_mode, if you returned a SQLAlchemy model from your path operation,
    # it wouldn’t include the relationship data.
    # TODO: Figure this out.
    class Config:
        orm_mode = True


# Properties to return to client
class Recipe(RecipeInDBBase):
    pass


# Properties properties stored in DB
class RecipeInDB(RecipeInDBBase):
    pass
