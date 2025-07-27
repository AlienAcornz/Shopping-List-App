import pytest
import pytest_asyncio
import mongomock_motor
from .mongo_client import append_prices, get_price, insert_list, get_list, insert_item, remove_item
from ..api.schemas import ShoppingList, Item, LocalShoppingList

@pytest_asyncio.fixture
async def mock_db(monkeypatch): #Creates a mock mongodb after every test is ran
    mock_client = mongomock_motor.AsyncMongoMockClient()
    db = mock_client['shoppingdb']

    monkeypatch.setattr("backend.db.mongo_client.price_collection", db["prices"])
    monkeypatch.setattr("backend.db.mongo_client.list_collection", db["lists"])
    return db

@pytest.mark.asyncio
async def test_insert_list(mock_db):
    shopping_list = LocalShoppingList(
        name="Test List",
        list=[Item(name="Apple", quantity=2, unit="kg")]
    )

    token = await insert_list(shopping_list)

    result = await mock_db["lists"].find_one({"token": token})
    assert result is not None
    assert result["name"] == "Test List"
    assert result["list"][0]["name"] == "Apple"

@pytest.mark.asyncio
async def test_get_list_success(mock_db):
    token = "testtoken"
    await mock_db["lists"].insert_one({
        "name": "Fake List", "token": token, "list": [{"name": "Cheese", "quantity": 3, "unit": "kg"}]
    })

    result = await get_list(token)
    assert result == {
        "name": "Fake List", "token": token, "list": [{"name": "Cheese", "quantity": 3, "unit": "kg"}]
    }

@pytest.mark.asyncio
async def test_get_list_not_found(mock_db):
    result = await get_list("faketoken")
    assert result is None

@pytest.mark.asyncio
async def test_insert_item_success(mock_db):
    token = "testtoken"
    await mock_db["lists"].insert_one({
        "name": "List A", "token": token, "list": []
    })

    item = Item(name="Milk", quantity=1, unit="l")
    await insert_item(token, item)

    result = await mock_db["lists"].find_one({"token": token})
    assert result is not None
    assert result["list"][0] == {"name":"Milk", "quantity":1, "unit":"l"}

@pytest.mark.asyncio
async def test_insert_item_not_found(mock_db):
    token = "faketoken"

    item = Item(name="Milk", quantity=1, unit="l")
    await insert_item(token, item)
    result = await mock_db["lists"].find_one({"token": token})
    assert result is None

@pytest.mark.asyncio
async def test_remove_item_success(mock_db):
    token = "testtoken"
    item = {"name": "Eggs", "quantity": 12, "unit": "each"}
    await mock_db["lists"].insert_one({
        "name": "List A", "token": token, "list": [item]
    })

    await remove_item(token, Item(**item))
    result = await mock_db["lists"].find_one({"token": token})
    assert item not in result["list"]

@pytest.mark.asyncio
async def test_remove_item_not_found(mock_db):
    token = "testtoken"
    await mock_db["lists"].insert_one({
        "name": "List A", "token": token, "list": []
    })

    item = Item(name="Bread", quantity=17, unit="each")
    await remove_item(token, item)
    result = await mock_db["lists"].find_one({"token": token})
    assert result["list"] == []