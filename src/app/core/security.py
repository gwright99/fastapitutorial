from datetime import datetime, timedelta, timezone
from typing import List, MutableMapping, Optional, Union

import jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session

from app.core.config import settings
from app.core.hashing import Hasher
from app.models.user import User

JWTPayloadMapping = MutableMapping[
    str, Union[datetime, bool, str, List[str], List[int]]
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def authenticate(
    *,
    email: str,
    password: str,
    db: Session,
) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not Hasher.verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # to_encode = data.copy()
    # to_encode.update({"exp": expire})

    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
