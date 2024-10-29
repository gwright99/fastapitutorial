from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth = (Column(DateTime),)
    created = Column(DateTime, default=datetime.utcnow)  # This is bad.

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return (
            f"UserModel(id={self.id=}; first_name={self.first_name};"
            f"last_name={self.last_name};"
            f"birth={self.birth}; created={self.created})"
        )


users = [
    UserModel(first_name="Bob", last_name="Preston", birth=datetime(1980, 5, 2)),
    UserModel(first_name="Susan", last_name="Sage", birth=datetime(1979, 6, 12)),
]

session_maker = sessionmaker(bind=create_engine("sqlite://models.db"))


def create_users():
    with session_maker() as session:
        for user in users:
            print(f"{user.full_name=}")
            session.add(user)
        session.commit()


create_users()
