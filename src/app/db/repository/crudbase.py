# https://web.archive.org/web/20240720070755/https://christophergs.com/tutorials/ultimate-fastapi-tutorial-pt-7-sqlalchemy-database-setup/

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.base_class import Base

# Generics. Easier in Python3.12
# Bounding == "Whatever variable type fed in must be equal or subtype of the bound definition"
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

# TODO: THIS MECHANISM FEELS POWERFUL BUT I FIND GENERICS A BIT CONFUSING. REWATCH YOUTUBE VIDS ON
#   TOPIC, THEN WORK THROUGH ACTUALLY USING INSTANTIATED CLASSES.


# Models inheriting from CRUDBase will be defined with a SQLAlchemy model as the first argument,
# then the Pydantic model (aka schema) for creating and updating rows as the
# second and third arguments.
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):  # 1
    def __init__(self, model: Type[ModelType]):  # 2
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()  # 3

    # skip is offset
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()  # 4

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()  # 5
        db.refresh(db_obj)
        return db_obj


from app.db.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate, RecipeUpdate


# Defining a new CRUD class for Recipe. Pass in the associated SQLAlchemy Class & Pydantic models.
class CRUDRecipe(CRUDBase[Recipe, RecipeCreate, RecipeUpdate]):  # 1
    ...


# Then create the actual object
recipe = CRUDRecipe(Recipe)  # 2
