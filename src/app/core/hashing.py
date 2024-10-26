from dataclasses import dataclass

import bcrypt
from passlib.context import CryptContext

"""
Dataclass and setattr solution used to solve hashing logger error:

    >>> Hasher.get_password_hash("supersecret1234")
    (trapped) error reading bcrypt version
    Traceback (most recent call last):
    File "/home/deeplearning/fastapitutorial/venv/lib/python3.10/site-packages/passlib/handlers/bcrypt.py", line 620, in _load_backend_mixin
        version = _bcrypt.__about__.__version__
    AttributeError: module 'bcrypt' has no attribute '__about__'
    '$2b$12$2nBbe/fhuYjoxujpLYAQ.uFgxRheihMWPXKPgve0ycGB.BJVuWe/G'

Solution taken from here on Oct 26/24: https://github.com/pyca/bcrypt/issues/684
"""


@dataclass
class SolveBugBcryptWarning:
    __version__: str = getattr(bcrypt, "__version__")


setattr(bcrypt, "__about__", SolveBugBcryptWarning())

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)
