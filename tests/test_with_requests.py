import json

import requests

from models.models import Item

# TODO: Convert this pull the value from ENV VAR so I can test locally and it container the same way with requests.
ENDPOINT = "https://fastapi.grahamwrightk8s.net/tutorial"
ENDPOINT = "http://localhost:8080"


def test_root() -> None:
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


def test_add() -> None:
    payload = {"x": 2, "y": 4}
    response = requests.post(f"{ENDPOINT}/add2", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data == {"result": 6}


def test_items() -> None:
    response = requests.get(f"{ENDPOINT}/items")

    assert response.status_code == 200
    data = response.json()
    assert len(data.keys()) == 3


def test_items_get_item_by_id() -> None:
    response = requests.get(f"{ENDPOINT}/items/0")
    print(f"Response is: {response.json()}")

    assert response.status_code == 200
    # response.json() to convert returned JSON payload to python dictionary.
    # json.dumps() to convert dictionary to string representation.
    # Raw load the string to reconstitute it as an Item.
    # This seems convoluted, there must be a better way?
    item = Item.parse_raw(json.dumps(response.json()))

    assert item.name == "Hammer"
    assert item.price == 9.99
    assert item.count == 20
