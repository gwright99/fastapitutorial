import json

import requests

from models.models import Category, Item

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
    assert len(data.keys()) == 2  # 3


def test_items_get_item_by_id() -> None:
    response = requests.get(f"{ENDPOINT}/items/0")
    print(f"Response is: {response.json()}")

    assert response.status_code == 200
    # response.json() to convert returned JSON payload to python dictionary.
    # json.dumps() to convert dictionary to string representation.
    # Raw load the string to reconstitute it as an Item.
    # This seems convoluted, there must be a better way?
    # item = Item.parse_raw(json.dumps(response.json()))
    item = Item.parse_raw(response.text)

    assert item.name == "Hammer"
    assert item.price == 9.99
    assert item.count == 20


def test_items_get_item_by_id_fail() -> None:
    response = requests.get(f"{ENDPOINT}/items/526")
    print(f"Response is: {response.json()}")

    assert response.status_code == 404
    assert "does not exist" in response.text


def test_items_get_item_by_str_fail() -> None:
    response = requests.get(f"{ENDPOINT}/items/faketext")
    print(f"Response is: {response.json()}")

    assert response.status_code == 422
    assert "unable to parse string as an integer" in response.text


def test_get_item_nails() -> None:
    response = requests.get(f"{ENDPOINT}/items?name=Nails")
    print(f"Response is: {response.json()}")

    assert response.status_code == 200
    data = response.json()
    item = json.dumps(data["selection"][0])
    item = Item.parse_raw(item)
    assert item.count == 100


def test_add_item() -> None:
    payload = Item(name="Hacksaw", price=19.99, count=25, id=4, category=Category.TOOLS)
    # Use `data` instead of `json` since payload is already JSON-type
    response = requests.post(f"{ENDPOINT}/items", data=payload.json())

    assert response.status_code == 200
    assert "added" in response.json().keys()


def test_update_item() -> None:
    # This is wrong? Not a payload but need to use string query instead?
    payload = {"item_id": 0, "count": 25}
    # response = requests.put(url=f"{ENDPOINT}/items/update/0", data=payload)
    response = requests.put(url=f"{ENDPOINT}/items/0?count=25")
    print(f"Response is: {response.json()}")

    assert response.status_code == 200
    data = response.json()
    item = Item.parse_raw(json.dumps(data["updated"]))
    assert item.count == 25


def test_update_item() -> None:
    payload = Item(name="Hacksaw", price=19.99, count=25, id=4, category=Category.TOOLS)
    response = requests.delete(f"{ENDPOINT}/items/1", data=payload.json())
    print(f"Response is: {response.json()}")

    assert "deleted" in response.json().keys()


# print(requests.get("http://127.0.0.1:8080/items?count=20").json())
# print(requests.get("http://127.0.0.1:8080/items?count=Hello").json())
