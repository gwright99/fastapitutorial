from db.repository.user import create_new_user
from db.session import get_db
from fastapi import APIRouter, Depends, status
from schemas.user import ShowUser, UserCreate
from sqlalchemy.orm import Session

router = APIRouter()


class BadRequest(Exception):
    pass


# Uses Pydantic schema to ensure the provided data is legit (pswd min 4, correct email regex)
@router.post(
    "/users",
    response_model=ShowUser,
    status_code=status.HTTP_201_CREATED,
    responses={500: {"description": ""}},
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # https://stackoverflow.com/questions/58642528/displaying-of-fastapi-validation-errors-to-end-users
    # Creating same user twice generates a ResponseValidationError

    from psycopg2.errors import UniqueViolation
    from sqlalchemy.exc import IntegrityError

    try:
        print(f"{user=}")
        user = create_new_user(user=user, db=db)
        return user
    except IntegrityError as e:
        assert isinstance(e.orig, UniqueViolation)  # proves the original exception
        print(f"{e=}")
        print(f"{e.orig=}")
        raise BadRequest from e
