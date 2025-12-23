from motor.motor_asyncio import AsyncIOMotorClient
import secrets
from ..api.schemas import Item, LocalShoppingList

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["shoppingdb"]
price_collection = db["prices"]
list_collection = db["lists"]

async def append_prices(data: dict):
    """
    Used to append many price data at once.
    """
    await price_collection.insert_many(data)

async def get_price(name: str):
    """
    returns the name, price, unit, category of an item.
    May be later updated to take the quantity as an input
    """
    return await price_collection.find_one({"name": name},{"_id": 0})


async def insert_list(data: LocalShoppingList):
    """
    Adds a list to the list collection
    """
    token = secrets.token_urlsafe()

    shopping_list = {
        "name": data.name,
        "token": token,
        "list": [item.model_dump() for item in data.list] #converts the items in the list into a dictonary format to be stored
    }
    await list_collection.insert_one(shopping_list)
    return token


async def get_list(token: str):
    """
    Retrieves the list given the corresponding token.
    """
    return await list_collection.find_one({"token": token}, {"_id": 0})

async def insert_item(token: str, item: Item):
    """
    Adds an item to a list given a token
    """
    await list_collection.update_one(
        {"token": token},
        {"$push": {"list": item.model_dump()}}
    )

async def remove_item(token: str, item: Item):
    """
    removes an item in a list given a token
    """
    await list_collection.update_one(
        {"token": token},
        {"$pull": {"list" : {"name": item.name, "quantity": item.quantity, "unit": item.unit}}}
    )