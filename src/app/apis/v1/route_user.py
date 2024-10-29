from db.repository.user import create_new_user
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi.responses import JSONResponse
from schemas.user import ShowUser
from schemas.user import UserCreate
from sqlalchemy.orm import Session

router = APIRouter()


class BadRequest(Exception):
    pass


# Uses Pydantic schema to ensure the provided data is legit (pswd min 4, correct email regex)
@router.post(
    "/users",
    response_model=ShowUser,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": """For security purposes, will always send 201. Behind the scenes,
                      brand new emails would get an activation link while existing emails get an access
                      attempt notification."""
        }
    },
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # https://stackoverflow.com/questions/58642528/displaying-of-fastapi-validation-errors-to-end-users
    # Creating same user twice generates a ResponseValidationError / IntegrityError
    # Thinking ahead re: login best practices, capture the Validation error and send back 201.

    from psycopg2.errors import UniqueViolation
    from sqlalchemy.exc import IntegrityError

    # TODO: Add mechanism to make both try/except blocks take same amount of time (for security).
    try:
        print(f"{user=}")
        user = create_new_user(user=user, db=db)
        # return user
    except IntegrityError as e:
        # assert isinstance(e.orig, UniqueViolation)  # proves the original exception
        print(f"{e=}")
        print(f"{e.orig=}")
        # raise BadRequest from e
        # TO DO: Add some sort of notification event re: attempted access of already existing account.

    # Regardless of whether created or error caught, return same response.
    return JSONResponse(
        status_code=201,
        content={
            "message": f"Thanks for registering. A verification code has been sent to {user.email}."
        },
    )
