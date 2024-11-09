import os
from pathlib import Path
from typing import List, Optional, Union

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, EmailStr, field_validator
from pydantic_settings import BaseSettings

from app.schemas.user import UserBase

# WARNING! `Path(".")` uses the directory where the FastAPI invocation command came from; NOT relative to this file.
# E.g `~/fastapitutorial$ fastapi run src/app/main.py --port 5000 --reload`
# The command below works when .env is in the PROJ_ROOT (also works for peer `tests/` folder).
env_path = Path(".") / ".env"
print(f"Dotenv file located at: {env_path.resolve()}")
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    """
    Pydantic BaseSettings automatically looks for environment variables of the same name.
    No need to define `os.environ` since this is done automagically.
    """

    PROJECT_NAME: str = "FastAPI Tutorial"
    PROJECT_VERSION: str = "0.0.1"

    # DATABASE PROD (POSTGRES)
    POSTGRES_USER: str | None = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str | None = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tdd")
    POSTGRES_DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # DATABASE PROD (SQLITE)
    SQLITE_DATABASE_URL: str = "sqlite:////tmp/fastapi/prod.db"

    # DATABASE PROD (GENERIC)
    SQLALCHEMY_DATABASE_URL: str = f"{POSTGRES_DATABASE_URL}"

    # DATABASE TEST (SQLITE)
    TEST_DB_FILE: str = "/tmp/fastapi/test.db"
    TEST_DB_URL: str = f"sqlite:///{TEST_DB_FILE}"

    # JWT CONFIG
    JWT_SECRET_KEY: Optional[str] = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"  # new
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # in mins  #new

    # https://web.archive.org/web/20240720062221/https://christophergs.com/tutorials/ultimate-fastapi-tutorial-pt-8-project-structure-api-versioning/
    # API SETTINGS
    API_V1_STR: str = "/api/v1"

    # AUTH
    # Identifies the endpoint where a frontend must send user credentials to retrieve a token.
    # The `oauth2_scheme` binds a OAuth2PasswordBearer with this URL.
    # Any endpoint with a declared dependency on `oauth2_scheme` will look for a Bearer HTTP Header or
    # else throw a 401.
    # https://stackoverflow.com/questions/67307159/what-is-the-actual-use-of-oauth2passwordbearer
    AUTH_TOKEN_URL: str = f"{API_V1_STR}/auth/token"

    # CORS
    # e.g: '["http://localhost", "http://localhost:4200", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # TODO: Replace this with something better like Vault / K8s Secret
    # TODO: Figure out how to make this comparable between local testing and K8s.
    SUPERUSERS: List[UserBase] = [
        UserBase(
            full_name="admin1",
            email="admin1@admin.com",
            is_superuser=True,
            password=os.getenv("ADMIN1", "default"),
        ),
        UserBase(
            full_name="admin2",
            email="admin2@admin.com",
            is_superuser=True,
            password=os.getenv("ADMIN2", "default"),
        ),
    ]

    #   .../site-packages/pydantic/_internal/_config.py:291:
    # PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead.
    # Deprecated in Pydantic V2.0 to be removed in V3.0.
    # See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.9/migration/

    # class Config:
    #     # Specify that all config settings are case-sensitive.
    #     case_sensitive = True
    model_config = {"case_sensitive": True}


settings = Settings()
