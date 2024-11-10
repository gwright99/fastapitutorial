import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import app.crud as crud
import app.schemas as schemas
from app.core.auth import authenticate_user, create_access_token
from app.dependencies.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.auth import Token
from app.schemas.user import UserCreate201

# ------------------------------------------------------------------------------------
# Helper Variables
# ------------------------------------------------------------------------------------
router = APIRouter()
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------------------------
# TODO: Add mechanism to make both try/except blocks take same amount of time (for security).
@router.post(
    path="/token",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    description="""Verifies user's password and generates JWT.""",
)
def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Create a JWT once user supplies username/password via OAuth2 request form body.

    NOTE:
    Hackers can use timing-based tools to determine if an account exists (assumes you'll only
    execute a cryptologically expensive hash on a found account vs non-existing). As a result,
    the `authenticate_user` method has been modified to run a hash even if an account isnt found.
    """

    user = authenticate_user(
        email=form_data.username, password=form_data.password, db=db
    )
    if not user:
        print(f"{email=}")
        print(f"{password=}")
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {
        "access_token": create_access_token(sub=str(user.id)),
        "token_type": "bearer",
    }


@router.post(
    path="/signup",
    # response_model=UserCreate201,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "model": UserCreate201,
            "description": """For security purposes, alway returns 201.""",
        }
    },
)  # , response_model=schemas.ShowUser, status_code=201)
def create_user_signup(
    *,
    db: Session = Depends(get_db),
    user_in: schemas.user.UserCreate,
) -> JSONResponse:
    """
    NOTE:
    Sign up pages should not leak if a user already exists. Regardless if a user already exists or was just created:

    1. Return an HTTP 200 with messsage to check email address for a verification code.
    2. Privately log if a sign-up attempt occurred agains an already-existing email address.
    3. Modify the payload sent to the email account to inform user if a (potentially) malicious login attempted.
    """

    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        logger.warning(
            f"Potentially malicious login attempt on {user_in.email}. Warn client."
        )
    else:
        logger.info(f"Creating user with following details: {user_in}")
        crud.user.create(db=db, obj_in=user_in)

    # Regardless of whether created or error caught, return same response.
    return JSONResponse(
        status_code=201,
        content={
            "message": f"Thanks for registering. A verification code has been sent to {user_in.email}."
        },
    )


@router.get("/me", response_model=schemas.ShowUser)
def read_users_me(current_user: User = Depends(get_current_user)) -> User:
    """
    Fetch the current logged in user.
    """

    user = current_user
    return user
