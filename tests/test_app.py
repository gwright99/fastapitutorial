# `client` passed into test functions as function-level fixture from conftest.py
# See: https://docs.pytest.org/en/6.2.x/fixture.html#conftest-py-sharing-fixtures-across-multiple-files

ADD2_TEST_SET = [[1, 1, 2], [-1, 1, 0], [2, 4, 6]]


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


# def test_add2(client):
#     response = client.post(url="/add2", json={"x": 2, "y": 3})
#     assert response.status_code == 200
#     assert response.json() == {"result": 5}


def test_add2(client):
    for test in ADD2_TEST_SET:
        x, y, result = test

        response = client.post(url="/add2", json={"x": x, "y": y})
        assert response.status_code == 200
        assert response.json() == {"result": result}
