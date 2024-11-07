import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from tests.conftest import request_access_token  # client_auth

legitimate_user_creds = {
    "username": settings.SUPERUSERS[0].email,
    "password": settings.SUPERUSERS[0].password,
}

legitimate_user_creds2 = {
    "username": settings.SUPERUSERS[1].email,
    "password": settings.SUPERUSERS[1].password,
}

bad_user_creds = {
    "username": "foo",
    "password": "bar",
}


@pytest.mark.parametrize("creds", [legitimate_user_creds, legitimate_user_creds2])
def test_request_access_token_positive(creds):
    client: TestClient = request_access_token(creds)
    assert "authorization" in client.headers.keys()


@pytest.mark.parametrize("creds", [bad_user_creds])
def test_request_access_token_negative(creds):
    with pytest.raises(KeyError) as excinfo:
        request_access_token(creds)
    # assert str(excinfo.value) == "Failed to retrieve FastAPI access token.  # This would NOT match but next one did.
    assert excinfo.value.args[0] == "Failed to retrieve FastAPI access token."


@pytest.mark.parametrize(
    "client_auth",
    [legitimate_user_creds],
    indirect=True,
)
def test_token_protected_endpoint_success(client_auth) -> None:
    response = client_auth.get("/api/v1/recipes/recipe/all")
    assert response.status_code == 200


def test_protected_endpoint_with_no_token(client_anon) -> None:
    response = client_anon.get("/api/v1/recipes/recipe/all")

    assert response.status_code == 401
    print(response.json())
    assert response.json()["detail"] == "Not authenticated"


# def test_get_endpoint_list():
#     response = client.get("/", headers={
#         "Authorization": f'Bearer {os.environ["BEARER_TOKEN"]}'})
#     assert response.status_code == 200
#     assert response.json() == {"Available Endpoints": ENDPOINT_LIST}
