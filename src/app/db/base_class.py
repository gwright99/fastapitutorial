"""
# https://fastapitutorial.com/blog/database-connection-fastapi/
Every model will inherit this 'Base' class and we will utilize this base class to 
create all the database tables. Centralize all common logic related to tables in this class.
"""

from typing import Any

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative


# TODO: Figure out as_declarative
# Declaration of `id` here means that all derived Tables will have an `id` column.
@as_declarative()
class Base:
    id: Any
    __name__: str

    # to generate tablename from classname
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
