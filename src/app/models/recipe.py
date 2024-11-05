from typing import Any, Optional

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.properties import MappedColumn

from app.db.base_class import Base

# Original Definition
# class Recipe(Base):
#     id = Column(Integer, primary_key=True, index=True)
#     label = Column(String(256), nullable=False)
#     url = Column(String(256), index=True, nullable=True)
#     source = Column(String(256), nullable=True)
#     submitter_id = Column(Integer, ForeignKey("user.id"), nullable=True)
#     submitter = relationship("User", back_populates="recipes")


class Recipe(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    label: MappedColumn[str] = mapped_column(String(256), nullable=False)
    url: MappedColumn[str] = mapped_column(String(256), index=True, nullable=True)
    source: MappedColumn[Optional[str]] = mapped_column(String(256), nullable=True)
    submitter_id: MappedColumn[int] = mapped_column(
        Integer, ForeignKey("user.id"), nullable=True
    )
    submitter = relationship("User", back_populates="recipes")
