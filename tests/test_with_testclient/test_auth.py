import pytest

from app.core.config import settings
from tests.conftest import client_auth

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


@pytest.mark.parametrize(
    "client_auth",
    [legitimate_user_creds, legitimate_user_creds2],
    indirect=True,
)
def test_token_success(client_auth) -> None:

    print(f"Headers are: {client_auth.headers['authorization']}")
    assert not (client_auth.headers["authorization"]).endswith(" ")

    # result = response.json()
    # print(f"{result=}")
    # assert response.status_code == 200


# @pytest.mark.parametrize(
#     "client_auth",
#     [bad_user_creds],
#     indirect=True,
# )
def test_token_fail() -> None:

    with pytest.raises(KeyError) as excinfo:
        client_auth(bad_user_creds)
    assert str(excinfo.value == "Failed to retrieve FastAPI access token.")


# def test_get_endpoint_list():
#     response = client.get("/", headers={
#         "Authorization": f'Bearer {os.environ["BEARER_TOKEN"]}'})
#     assert response.status_code == 200
#     assert response.json() == {"Available Endpoints": ENDPOINT_LIST}


def test_protected_endpoint_with_no_token(client) -> None:
    response = client.get("/api/v1/recipes/recipe/all")

    assert response.status_code == 200
    assert response.json() == {"msg": "I aint dead!"}
