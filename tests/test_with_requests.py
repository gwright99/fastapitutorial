import requests

ENDPOINT = "https://fastapi.grahamwrightk8s.net/tutorial"


def test_root() -> None:
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


def test_add() -> None:
    payload = {"x": 2, "y": 4}
    response = requests.post(f"{ENDPOINT}/add2", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data == {"result": 6}
