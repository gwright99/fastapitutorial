"""
# https://fastapitutorial.com/blog/database-connection-fastapi/
Every model will inherit this 'Base' class and we will utilize this base class to
create all the database tables. Centralize all common logic related to tables in this class.
"""
from typing import Any

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative

metadata_obj = MetaData()


# TODO: Figure out as_declarative
# Declaration of `id` here means that all derived Tables will have an `id` column.
@as_declarative()
class Base:
    id: Any
    # I think this solves the metadata Pylance errors -- would automatically be created if I didn't declare but
    # that seems to piss of Pylance static type checker:
    # https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.as_declarative_base
    metadata = metadata_obj
    __name__: str

    # to generate tablename from classname. Prevents needing to declare on every Class like:
    # __tablename__ = 'some_value'
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
