import os
from pathlib import Path

from dotenv import load_dotenv

# WARNING! `Path(".")` using the directory where the FastAPI invocation command came from,
# NOT relative to this file. E.g "~/fastapitutorial" or "~/fastapitutorial/tests" #
# (where invocation would be `fastapi run ../src/app/app.py --port 8080 --reload`)
# The command below works when .env is in the PROJ_ROOT.
env_path = Path(".") / ".env"
print(f"Dotenv file located at: {env_path.resolve()}")
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "FastAPI Tutorial"
    PROJECT_VERSION: str = "0.0.1"

    POSTGRES_USER: str | None = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str | None = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: int = int(
        os.getenv("POSTGRES_PORT", 5432)
    )  # default postgres port is 5432
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tdd")
    DATABASE_URL: str = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    # SQLITE
    # DATABASE_URL: str = "/tmp/fastapitutorial.db"

    # JWT CONFIG
    SECRET_KEY: str = os.getenv("SECRET_KEY")  # new
    ALGORITHM = "HS256"  # new
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # in mins  #new


settings = Settings()
