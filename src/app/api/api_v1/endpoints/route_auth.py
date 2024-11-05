from typing import Any

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import app.crud as crud
import app.schemas as schemas
from app.core.auth import authenticate_user, create_access_token, oauth2_scheme
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import Token, TokenData

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
# Helper Functions
# ------------------------------------------------------------------------------------
# This function feels a little over-engineered but maybe designed this way for future extensions?
# Aka crack-the-token-and-look-inside.
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


# ------------------------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------------------------
@router.post("/token", response_model=Token)
def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Create a JWT once user supplies username/passwrod via OAuth2 request form body.
    """

    user = authenticate_user(
        email=form_data.username, password=form_data.password, db=db
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {
        "access_token": create_access_token(sub=str(user.id)),
        "token_type": "bearer",
    }


@router.post("/signup", response_model=schemas.User, status_code=201)
def create_user_signup(
    *,
    db: Session = Depends(get_db),
    user_in: schemas.user.UserCreate,
) -> Any:
    """
    Create new user without the need to be logged in.
    """

    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(  # 5
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user = crud.user.create(db=db, obj_in=user_in)  # 6

    return user


@router.get("/me", response_model=schemas.ShowUser)
def read_users_me(current_user: User = Depends(get_current_user)) -> User:
    """
    Fetch the current logged in user.
    """

    user = current_user
    return user
