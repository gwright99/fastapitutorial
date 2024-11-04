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


# `as_declarative() is same as `Base = declarative_base()` but using the decorator approach means
# we can also declare helper methods / attributes that all inheriting tables will get automagically.
@as_declarative()
class Base:
    id: Any
    # I think this solves the metadata Pylance errors -- would automatically be created if I didn't declare but
    # that seems to piss of Pylance static type checker:
    # https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.as_declarative_base
    metadata = metadata_obj
    __name__: str

    # Original code used the decorator: `@declared_attr`. This caused MyPy to go nuts.
    # As per https://github.com/sqlalchemy/sqlalchemy/issues/9213 (which pointed to: https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr),
    # It actually needed two things:
    #  1) Explicit definition of `@classmethod`
    #  2) Modify attribute decorator with `.directive` (indicates it's not a Mapped attribute).
    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
