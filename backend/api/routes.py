from fastapi import FastAPI, HTTPException
from ..db.mongo_client import getPrice

api = FastAPI()

@api.get('/price/{item}')
async def get_item(item: str):
    return await getPrice(item)