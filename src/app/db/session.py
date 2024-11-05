from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from app.core.auth import oauth2_scheme
from app.core.config import settings

# ------------------------------------------------------------------------------------
# Helper Variables
# ------------------------------------------------------------------------------------
# FastAPI can access db with multiple threads during a single request; must configure SQLite to allow.
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
# engine = create_engine( SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# TODO: pre-warmed connection pool?
print(f"{settings.SQLALCHEMY_DATABASE_URL=}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Generate session for dependency injection (can be subbed out at testing time).
def get_db() -> Generator:
    try:
        db: Session = SessionLocal()
        yield db
    finally:
        db.close()  # type: ignore   <-- suppress Pylance 'possibly unbound' error
