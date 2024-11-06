from typing import Generator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient  # <--- emulation of endpoints

from app.core.config import settings
from app.dependencies.dependencies import get_reddit_client
from app.main import app


# ---- Move to conftest
async def override_reddit_dependency() -> MagicMock:
    """
    This creates a mock Reddit client.
    The mock client has one method `get_reddit_top` which returns a hard-coded value.
    This mock client is jammed into the TestClient via the client generating fixture below.
    """
    mock = MagicMock()  # 4
    reddit_stub = {
        "recipes": [
            "baz",
        ],
        "easyrecipes": [
            "bar",
        ],
        "TopSecretRecipes": ["foo"],
    }
    # This allows us to replace behaviours of real values in real functions, AND/OR
    # Create completely fake methods / attributes not supported by real client (e.g. `saya`)
    mock.get_reddit_top.return_value = reddit_stub
    # mock.saya.return_value = "aaa"   # add `    print(reddit_client.saya())` in called endpoint and run test.
    return mock


@pytest.fixture()
def client() -> Generator:
    with TestClient(app) as client:
        # Replace the dependency (left) with the one on the right
        app.dependency_overrides[get_reddit_client] = override_reddit_dependency
        yield client
        app.dependency_overrides = {}


# ------------------


def test_fetch_ideas_reddit_sync(client):  # 1
    # When
    response = client.get(f"{settings.API_V1_STR}/recipes/ideas/")
    data = response.json()

    # Then
    assert response.status_code == 200
    for key in data.keys():
        assert key in ["recipes", "easyrecipes", "TopSecretRecipes"]
