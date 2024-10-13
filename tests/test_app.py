from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthcheck():
    response = client.get("/healthcheck")
    # response = root_client.get("/healthcheck")
    print("testing")
    assert response.status_code == 200
    assert response.json() == {"msg": "I aint dead!"}


def test_root():
    print("client_base_url: ", client.base_url)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World!"}
