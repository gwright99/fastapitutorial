from app.core.config import settings


def test_token_success(client) -> None:
    """
    curl -X 'POST' \
        'http://localhost:5000/tutorial/api/v1/auth/token' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/x-www-form-urlencoded' \
        -d 'grant_type=password&username=fake&password=user&scope=&client_id=string&client_secret=string'
  """

    # https://stackoverflow.com/questions/75042410/fastapi-testclient-not-able-to-send-post-request-using-form-data
    form_data = {
        "username": settings.SUPERUSERS[0].email,
        "password": settings.SUPERUSERS[0].password,
    }

    response = client.post(
        url=settings.AUTH_TOKEN_URL,
        data=form_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    result = response.json()
    print(f"{result=}")
    assert response.status_code == 200
