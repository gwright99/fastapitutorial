from typing import Optional

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app


# # ---------------------------------------------------------------------------------------------
# def pytest_configure(config):
#     """
#     Allows plugins and conftest files to perform initial configuration.
#     This hook is called for every plugin and initial conftest
#     file after command line options have been parsed.
#     """
#     pass
# def pytest_sessionstart(session):
#     """
#     Called after the Session object has been created and
#     before performing collection and entering the run test loop.
#     """
#     # https://stackoverflow.com/questions/27844088/python-get-directory-two-levels-up
#     # Assumes following path: .. > installer > tests > conftest.py
#     # import sys
#     # from pathlib import Path
#     # grandparent_dir = Path(__file__).resolve().parents[2]
#     # sys.path.append(str(grandparent_dir))
#     pass
# def pytest_sessionfinish(session, exitstatus):
#     """
#     Called after whole test run finished, right before
#     returning the exit status to the system.
#     """
#     pass
# def pytest_unconfigure(config):
#     """
#     Called before test process is exited.
#     """
#     pass
# # ---------------------------------------------------------------------------------------------
def request_access_token(creds: dict[str, str]) -> TestClient:
    """
    curl -X 'POST' \
        'http://localhost:5000/tutorial/api/v1/auth/token' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/x-www-form-urlencoded' \
        -d 'grant_type=password&username=fake&password=user&scope=&client_id=string&client_secret=string'

    result={
        'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxN...', 
        'token_type': 'bearer'}
    """
    client: TestClient = TestClient(app)

    form_data = {
        "username": creds["username"],
        "password": creds["password"],
    }

    response = client.post(
        url=settings.AUTH_TOKEN_URL,
        data=form_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    if access_token := response.json().get("access_token", None):
        auth_header = {"Authorization": f"Bearer {access_token}"}
        return TestClient(app, headers=auth_header)
    else:
        raise KeyError("Failed to retrieve FastAPI access token.")


@pytest.fixture(scope="function", autouse=False)
def client_anon() -> TestClient:
    print("Creating TestClient")
    return TestClient(app)


@pytest.fixture(scope="function", autouse=False)
def client_auth(request) -> TestClient:
    # def get_token_header(username: str, password: str) -> dict:
    """
    Call this fixture via:
      @pytest.mark.parametrize('client_auth', [legitimate_user_creds, ...], indirect=True)
      def test_some_test_function(self, client_auth):
    """
    return request_access_token(request.param)

    # form_data = {
    #     "username": request.param["username"],
    #     "password": request.param["password"],
    # }


# def get_token_header(username: str, password: str) -> dict:
#     """
#     curl -X 'POST' \
#         'http://localhost:5000/tutorial/api/v1/auth/token' \
#         -H 'accept: application/json' \
#         -H 'Content-Type: application/x-www-form-urlencoded' \
#         -d 'grant_type=password&username=fake&password=user&scope=&client_id=string&client_secret=string'

#     result={
#         'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxN...',
#         'token_type': 'bearer'}
#     """
#     local_client: TestClient = client()

#     form_data = {
#         "username": username,
#         "password": password,
#     }

#     response = local_client.post(
#         url=settings.AUTH_TOKEN_URL,
#         data=form_data,
#         headers={"Content-Type": "application/x-www-form-urlencoded"},
#     )

#     return {"Authorization": f"Bearer {response.json()['access_token']}"}


# def test_get_list(client, test_user):
#     token = test_login(client, test_user)
#     response = client.get("/lists/1", headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 200
#     assert response.json()["id"] == 1


# result = response.json()
# print(f"{result=}")
# assert response.status_code == 200
