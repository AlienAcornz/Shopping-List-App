from fastapi import FastAPI, HTTPException
from ..db.mongo_client import get_price, insert_list, get_list, insert_item, remove_item
from .schemas import Item, PriceResponse, ShoppingList, TokenResponse, LocalShoppingList
api = FastAPI()

@api.get('/price/{item}', response_model=PriceResponse)
async def get_item(item: str):
    """
    Gets the price of a given item.
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
    if result.modified_count == 0:
        raise HTTPException(404, "List not found.")
    return {"status": "item added"}

@api.delete('/list/{token}/items')
async def remove_item_from_list(token: str, item: Item):
    """
    Removes an item from a list given the token
    """
    result = await remove_item(token, item)
    if result.modified_count == 0:
        raise HTTPException(404, "List not found.")
    return {"status": "item removed"}