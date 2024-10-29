from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Optional

import jwt
from core.config import settings


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
