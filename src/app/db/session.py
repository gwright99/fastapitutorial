import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# ------------------------------------------------------------------------------------
# Helper Variables
# ------------------------------------------------------------------------------------
# Attempt to generate a SessionLocal that can support both PROD and TESTING flows with minimal changes.

# FastAPI can access db with multiple threads during a single request; must configure SQLite to allow this.
if os.getenv("FASTAPI_TESTING_RUN_ACTIVE", False):
    print("******* TESTING ACTIVE****")
    engine = create_engine(
        settings.TEST_DB_URL, connect_args={"check_same_thread": False}
    )

elif "postgresql://" in settings.SQLALCHEMY_DATABASE_URL:
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)

elif "sqlite://" in settings.SQLALCHEMY_DATABASE_URL:
    # FastAPI can access db with multiple threads during a single request; must configure SQLite to allow
    print("******* SQLITE ACTIVE****")
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    raise Exception("Cannot determine DB engine.")

# TODO: pre-warmed connection pool?
print(f"{settings.SQLALCHEMY_DATABASE_URL=}")
print(f"{settings.TEST_DB_URL=}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
