import os
from pathlib import Path
from typing import List, Optional, Union

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, EmailStr, field_validator
from pydantic_settings import BaseSettings

# WARNING! `Path(".")` using the directory where the FastAPI invocation command came from,
# NOT relative to this file. E.g "~/fastapitutorial" or "~/fastapitutorial/tests" #
# (where invocation would be `fastapi run ../src/app/app.py --port 8080 --reload`)
# The command below works when .env is in the PROJ_ROOT.
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

    # POSTGRES DB
    POSTGRES_USER: str | None = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str | None = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: int = int(
        os.getenv("POSTGRES_PORT", 5432)
    )  # default postgres port is 5432
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tdd")
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # SQLITE DB
    # DATABASE_URL: Optional[str] = "/tmp/fastapitutorial.db"

    # JWT CONFIG
    SECRET_KEY: Optional[str] = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"  # new
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # in mins  #new

    # https://web.archive.org/web/20240720062221/https://christophergs.com/tutorials/ultimate-fastapi-tutorial-pt-8-project-structure-api-versioning/
    # API SETTINGS
    API_V1_STR: str = "/api/v1"

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

    # Super Use Setup
    FIRST_SUPERUSER: EmailStr = "admin@recipeapi.com"

    class Config:
        # Specify that all config settings are case-sensitive.
        case_sensitive = True


settings = Settings()
