from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["shoppingdb"]
price_collection = db["prices"]


async def appendPrices(data: dict):
    """
    Used to append a dictonary of prices that were scraped.
    """
    await price_collection.insert_many(data)

async def getPrice(name: str) -> dict:
    """
    returns the name, price, unit, category of an item.
    May be later updated to take the quantity as an input
    """
    return await price_collection.find_one({"name": name},{"_id": 0})


