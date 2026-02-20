from fastapi import FastAPI, HTTPException
from ..db.mongo_client import get_price, insert_list, get_list, insert_item, remove_item, get_db
from .schemas import Item, PriceResponse, ShoppingList, TokenResponse, LocalShoppingList
from fastapi.middleware.cors import CORSMiddleware
from ..db.prices.normalize_prices import loadData, searchItem

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_data = {}

@api.on_event("startup")
async def get_init_data():
    print("Initializing data...")
    init_data["X"], init_data["vectorizer"], init_data["phraser"], init_data["db"] = await loadData()


@api.get('/priceold/{item}', response_model=PriceResponse)
async def old_get_item(item: str):
    """
    ===DEPRETIATED===Gets the price of a given item.
    """
    result =  await get_price(item)
    if not result:
        raise HTTPException(status_code=404, detail=f"Item '{item}' not found.")
    return result

@api.post('/list/create', response_model=TokenResponse)
async def create_shopping_list(payload: LocalShoppingList):
    """
    Shares a shopping list to the cloud
    """
    token = await insert_list(payload)
    return {"token": token}

@api.get('/list/{token}', response_model=ShoppingList)
async def get_shopping_list(token: str):
    """
    Gets the list given the token.
    """
    result = await get_list(token)

    if not result:
        raise HTTPException(status_code=404, detail=f"List not found.")
    return result

@api.post('/list/{token}/items')
async def add_item_to_list(token: str, item: Item):
    """
    Adds an item to a list given the token
    """
    result = await insert_item(token, item)
    if not result or result.modified_count == 0:
        raise HTTPException(404, "List not found.")
    return {"status": "item added"}

@api.delete('/list/{token}/items')
async def remove_item_from_list(token: str, item: Item):
    """
    Removes an item from a list given the token
    """
    result = await remove_item(token, item)
    if not result or result.modified_count == 0:
        raise HTTPException(404, "List not found.")
    return {"status": "item removed"}

@api.post('/price', response_model=PriceResponse)
async def get_item(item: Item):
    if item.unit not in ["kg", "g", "ml", "cl", "l", "each"]:
        raise HTTPException(404, "Invalid unit given")
    result = await searchItem(userInput=item.name, vectorizer=init_data["vectorizer"], phraser=init_data["phraser"], X=init_data["X"], db=init_data["db"])

    price = 0
    if item.unit in ["kg", "g"]:
        price = result["price_per_kilo"]
    elif item.unit in ["l", "ml", "cl"]:
        price = result["price_per_litre"]
    elif item.unit == "each":
        price = result["price_per_each"]

    if item.unit in ["ml", "g"]:
        price = round(price / 1000, 2)
    
    if item.unit == "cl":
        price = round(price / 100, 2)

    return PriceResponse(name=result["name"], price=price, unit=item.unit, category=result["category"])