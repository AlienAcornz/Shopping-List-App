from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    name: str
    quantity: int
    unit: str

class ShoppingList(BaseModel):
    name: str
    token: str
    list: List[Item]

class LocalShoppingList(BaseModel):
    name: str
    list: List[Item]

class PriceResponse(BaseModel):
    name: str
    price: float
    unit: str
    category: str

class TokenResponse(BaseModel):
    token: str