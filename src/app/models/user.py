from typing import List

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)  # I left out ()
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)  # I left out ()
    # If I had "Blog" in same file, this should work. Since they are separated, I cant make this work
    # due to circular importing. Leave this relationship typing off.
    # blogs: Mapped[List["Blog"]] = relationship("Blog", back_populates="author")  # type: ignore
    blogs = relationship("Blog", back_populates="author")
    # TODO: Find out what this does.
    recipes = relationship(
        "Recipe",
        cascade="all,delete-orphan",
        back_populates="submitter",
        uselist=True,
    )


# class User(Base):
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, nullable=False, unique=True, index=True)
#     password = Column(String, nullable=False)
#     is_superuser = Column(Boolean, default=False)  # I left out ()
#     is_active = Column(Boolean, default=True)  # I left out ()
#     blogs = relationship("Blog", back_populates="author")
