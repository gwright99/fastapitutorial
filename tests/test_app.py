# `client` passed into test functions as function-level fixture from conftest.py
# See: https://docs.pytest.org/en/6.2.x/fixture.html#conftest-py-sharing-fixtures-across-multiple-files


def test_healthcheck(client):
    response = client.get("/healthcheck")
    print("testing")
    assert response.status_code == 200
    assert response.json() == {"msg": "I aint dead!"}


def test_root(client):
    print("client_base_url: ", client.base_url)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World!"}
