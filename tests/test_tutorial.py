# These local values didn't work because they were getting overridden by stuff in conftest.py
from typing import Any
from typing import Generator

import pytest
from apis.base import api_router
from db.base import Base
from db.session import get_db
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def start_application():
    app = FastAPI()
    app.include_router(api_router)
    return app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
# Use connect_args parameter only with sqlite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the tables.
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    # Notice how this monkeypatches `get_db`
    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


def test_create_user(client):
    data = {"email": "testuser@nofoobar.com", "password": "testing"}
    response = client.post("/users", json=data)
    assert response.status_code == 201
    assert "Thanks for registering." in response.text
    # assert response.json()["email"] == "testuser@nofoobar.com"
    # assert response.json()["is_active"] == True

    data = {"email": "testuser@nofoobar.com", "password": "testing"}
    response = client.post("/users", json=data)
    assert response.status_code == 201
    assert "Thanks for registering." in response.text
    # assert response.json()["email"] == "testuser@nofoobar.com"
    # assert response.json()["is_active"] == True


from tests.utils.blog import create_random_blog


def test_should_fetch_blog_created(client, db_session):
    blog = create_random_blog(db=db_session)
    # print(blog.__dict__)    #use pytest -s to see print statements
    response = client.get(f"blog/{blog.id}/")
    assert response.status_code == 200
    assert response.json()["title"] == blog.title
