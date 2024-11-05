from typing import Optional

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

# Original Definition
# class User(Base):
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, nullable=False, unique=True, index=True)
#     password = Column(String, nullable=False)
#     is_superuser = Column(Boolean, default=False)  # I left out ()
#     is_active = Column(Boolean, default=True)  # I left out ()
#     blogs = relationship("Blog", back_populates="author")


# This new technique is to avoid Pylance errors like:
# "Column[int]" is not assignable to "int"
class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[Optional[str]]
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    # password: Mapped[str] = mapped_column(String, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)  # I left out ()
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)  # I left out ()
    # If "Blog" class in same file, this should work. Since they are separated, I cant make this work
    # due to circular importing. Leave left-side definitions off and use right-side relationship forward
    # references.
    # blogs: Mapped[List["Blog"]] = relationship("Blog", back_populates="author")  # type: ignore
    blogs = relationship("Blog", back_populates="author")
    # TODO: Find out what this does.
    recipes = relationship(
        "Recipe",
        cascade="all,delete-orphan",
        back_populates="submitter",
        uselist=True,
    )

    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
