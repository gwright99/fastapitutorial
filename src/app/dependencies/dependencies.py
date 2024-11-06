from typing import Generator

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.crud as crud
from app.clients.reddit import RedditClient
from app.core.auth import oauth2_scheme
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.auth import TokenData

# ------------------------------------------------------------------------------------
# Helper Variables
# ------------------------------------------------------------------------------------
router = APIRouter()

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


# ------------------------------------------------------------------------------------
# Database
# ------------------------------------------------------------------------------------
# Generate session for dependency injection (can be subbed out at testing time).
def get_db() -> Generator:
    try:
        db: Session = SessionLocal()
        yield db
    finally:
        db.close()  # type: ignore   <-- suppress Pylance 'possibly unbound' error


# ------------------------------------------------------------------------------------
# Clients
# ------------------------------------------------------------------------------------
def get_reddit_client() -> RedditClient:
    return RedditClient()


# ------------------------------------------------------------------------------------
# User / Session
# ------------------------------------------------------------------------------------
# This function feels a little over-engineered but maybe designed this way for future extensions?
# Aka crack-the-token-and-look-inside.
# NOTE: This dependency has its own dependency! (i.e. user must be logged in).
async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_aud": False},
        )
    # except jwt.exceptions.InvalidTokenError:
    except jwt.exceptions.PyJWTError as e:
        print(f"error! {e}")
        raise CREDENTIALS_EXCEPTION

    # Extract user id number from token.
    username: str = payload.get("sub")
    if username is None:
        raise CREDENTIALS_EXCEPTION
    token_data = TokenData(username=username)

    # Retrieve User from db based on token id (sub) value.
    user = db.query(User).filter(User.id == token_data.username).first()
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user


# Increase the specificity of our authorization to restricts to only superusers.
def caller_has_superuser_status(
    current_user: User = Depends(get_current_user),
) -> User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
