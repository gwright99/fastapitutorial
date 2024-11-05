from typing import Generator, Optional

import jwt
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from app.core.config import settings
from app.core.security import oauth2_scheme
from app.models.user import User

SQLALCHEMY_DATABASE_URL: str = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# FastAPI can access db with multiple threads during a single request; must configure SQLite to allow.
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# engine = create_engine( SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# TODO: Investigate what this does specifically
# The sessionmaker class is normally used to create a top level Session configuration
# which can then be used throughout an application without the need to repeat the
# configurational arguments.
# TODO: pre-warmed connection pool?
print(f"{SQLALCHEMY_DATABASE_URL=}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class TokenData(BaseModel):
    username: Optional[str] = None


# Generate session for dependency injection (can be subbed out at testing time).
def get_db() -> Generator:
    try:
        db: Session = SessionLocal()
        yield db
    finally:
        db.close()  # type: ignore   <-- suppress Pylance 'possibly unbound' error


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.exceptions.InvalidTokenError:
        raise credentials_exception

    user = db.query(User).filter(User.id == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user
