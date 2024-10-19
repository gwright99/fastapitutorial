# `client` passed into test functions as function-level fixture from conftest.py
# See: https://docs.pytest.org/en/6.2.x/fixture.html#conftest-py-sharing-fixtures-across-multiple-files

ADD2_TEST_SET = [[1, 1, 2], [-1, 1, 0], [2, 4, 6]]


def test_root(client) -> None:
    """
    Test the root path of the FastAPI app.

    Args:
        client: Fixture to create FastAPI TestClient.

    Returns: None
    """
    print("client_base_url: ", client.base_url)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World!"}


def test_healthcheck(client) -> None:
    """
    Test the /healthcheck path of the FastAPI app.

    Args:
        client: Fixture to create FastAPI TestClient.

    Returns: None
    """
    response = client.get("/healthcheck")
    print("testing")
    assert response.status_code == 200
    assert response.json() == {"msg": "I aint dead!"}


def test_add2(client) -> None:
    """
    Test the `/add2` function.

    Args:
        client: Fixture to create FastAPI TestClient.

    Returns: None
    """
    for test in ADD2_TEST_SET:
        x, y, result = test

        response = client.post(url="/add2", json={"x": x, "y": y})
        assert response.status_code == 200
        assert response.json() == {"result": result}
