from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import app.crud as crud
import app.schemas as schemas
from app.core.security import authenticate, create_access_token
from app.db.session import get_current_user, get_db
from app.models.user import User

router = APIRouter()


@router.post("/login")
def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """

    user = authenticate(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {
        "access_token": create_access_token(sub=str(user.id)),
        "token_type": "bearer",
    }


@router.post("/signup", response_model=schemas.User, status_code=201)
def create_user_signup(
    *,
    db: Session = Depends(get_db),  # 2
    user_in: schemas.user.UserCreate,  # 3
) -> Any:
    """
    Create new user without the need to be logged in.
    """

    user = db.query(User).filter(User.email == user_in.email).first()  # 4
    if user:
        raise HTTPException(  # 5
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user = crud.user.create(db=db, obj_in=user_in)  # 6

    return user


@router.get("/me", response_model=schemas.ShowUser)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Fetch the current logged in user.
    """

    user = current_user
    return user
