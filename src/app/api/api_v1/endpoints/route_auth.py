from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import app.crud as crud
import app.schemas as schemas
from app.core.auth import authenticate_user, create_access_token
from app.dependencies.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.auth import Token

# ------------------------------------------------------------------------------------
# Helper Variables
# ------------------------------------------------------------------------------------
router = APIRouter()


# ------------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------------


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


@router.post("/signup", response_model=schemas.ShowUser, status_code=201)
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
