import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from .routes import api

client = TestClient(api)


def test_create_shopping_list():
    with patch("backend.api.routes.insert_list", new=AsyncMock(return_value="mockedtoken")): #creates a mock of the api
        payload = {
            "name": "Weekly",
            "list": [{"name": "Apple", "quantity": 1, "unit": "kg"}]
        }
        resp = client.post("/list/create", json=payload)

    assert resp.status_code == 200
    assert resp.json() == {"token": "mockedtoken"}


def test_get_shopping_list_success():
    fake = {
        "name": "Test List",
        "token": "testtoken",
        "list": [{"name": "Cheese", "quantity": 2, "unit": "kg"}]
    }
    with patch("backend.api.routes.get_list", new=AsyncMock(return_value=fake)):
        resp = client.get("/list/testtoken")

    assert resp.status_code == 200
    assert resp.json() == fake


def test_get_shopping_list_not_found():
    with patch("backend.api.routes.get_list", new=AsyncMock(return_value=None)):
        resp = client.get("/list/invalidtoken")

    assert resp.status_code == 404
    assert resp.json()["detail"] == "List not found."


def test_add_item_to_list_success():
    # insert_item returns an object with modified_count attribute
    class R: modified_count = 1

    with patch("backend.api.routes.insert_item", new=AsyncMock(return_value=R())):
        resp = client.post(
            "/list/testtoken/items",
            json={"name": "Milk", "quantity": 2, "unit": "l"}
        )

    assert resp.status_code == 200
    assert resp.json() == {"status": "item added"}


def test_add_item_to_list_not_found():
    class R: modified_count = 0

    with patch("backend.api.routes.insert_item", new=AsyncMock(return_value=R())):
        resp = client.post(
            "/list/testtoken/items",
            json={"name": "Milk", "quantity": 2, "unit": "l"}
        )

    assert resp.status_code == 404
    assert resp.json()["detail"] == "List not found."


def test_remove_item_from_list_success():
    class R: modified_count = 1

    with patch("backend.api.routes.remove_item", new=AsyncMock(return_value=R())):
        resp = client.request(
            "DELETE",
            "/list/testtoken/items",
            json={"name": "Eggs", "quantity": 12, "unit": "each"}
        )

    assert resp.status_code == 200
    assert resp.json() == {"status": "item removed"}


def test_remove_item_from_list_not_found():
    class R: modified_count = 0

    with patch("backend.api.routes.remove_item", new=AsyncMock(return_value=R())):
        resp = client.request(
            "DELETE",
            "/list/testtoken/items",
            json={"name": "Eggs", "quantity": 12, "unit": "each"}
        )

    assert resp.status_code == 404
    assert resp.json()["detail"] == "List not found."