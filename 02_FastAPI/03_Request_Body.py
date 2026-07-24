from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# ----------------------------
# Request Body Model
# ----------------------------
class Item(BaseModel):
    name: str
    price: float
    description: str | None = None
    tax: float | None = None


# ----------------------------
# GET Request (Path Parameter)
# ----------------------------
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {
        "message": "Item fetched successfully",
        "item_id": item_id
    }


# ----------------------------
# GET Request (Query Parameters)
# ----------------------------
@app.get("/search")
async def search_items(skip: int = 0, limit: int = 10):
    return {
        "skip": skip,
        "limit": limit
    }


# ----------------------------
# POST Request (Request Body)
# ----------------------------
@app.post("/items")
async def create_item(item: Item):

    return {
        "message": "Item created successfully",
        "item": item
    }