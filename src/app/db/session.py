from typing import Generator

from core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

SQLALCHEMY_DATABASE_URL: str = settings.DATABASE_URL
print(f"{SQLALCHEMY_DATABASE_URL=}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# Necessary to work with SQLite - this is a common gotcha because FastAPI can access
# the database with multiple threads during a single request, so SQLite needs to be configured
# to allow that.

# TODO: Investigate what this does specifically
# The sessionmaker class is normally used to create a top level Session configuration
# which can then be used throughout an application without the need to repeat the
# configurational arguments.
# TODO: pre-warmed connection pool?
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Generate session for dependency injection (can be subbed out at testing time).
def get_db() -> Generator:
    try:
        db: Session = SessionLocal()
        yield db
    finally:
        db.close()  # type: ignore   <-- suppress Pylance 'possibly unbound' error
