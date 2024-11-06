from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session

from app.core.config import settings
from app.core.hashing import Hasher
from app.models.user import User
from app.typeslocal.types import JWTPayloadMapping

# Any endpoint with a declared dependency on `oauth2_scheme` will look for a Bearer HTTP Header or
# else throw a 401.
# https://stackoverflow.com/questions/67307159/what-is-the-actual-use-of-oauth2passwordbearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.AUTH_TOKEN_URL}")


def authenticate_user(
    *,
    email: str,
    password: str,
    db: Session,
) -> Optional[User]:
    """
    NOTE:
    Hackers can use timing-based tools to determine if an account exists (assumes you'll only
    execute a cryptologically expensive hash on a found account vs non-existing).

    In cases were `user` not found, run a hash on a fake password before returning None.
    """

    # Return None if User does not exist or password is wrong.
    user = db.query(User).filter(User.email == email).first()
    if not user:
        # hashed_password is "lorem"
        Hasher.verify_password(
            "ipsem", "$2b$12$jGWwfRodNgpUgFjbKvcz7O8Nf3MprXG5lHXQRHxH64ciQAqtNIH4m"
        )
        return None

    if not Hasher.verify_password(password, user.hashed_password):
        return None

    return user


def create_access_token(*, sub: str) -> str:
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def _create_token(
    token_type: str,
    lifetime: timedelta,
    sub: str,
) -> str:
    payload: JWTPayloadMapping = {}
    expiry = datetime.now(timezone.utc) + lifetime

    payload["type"] = token_type
    payload["exp"] = expiry
    payload["iat"] = datetime.now(timezone.utc)
    payload["sub"] = str(sub)

    encoded_jwt = jwt.encode(
        payload=payload, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt
