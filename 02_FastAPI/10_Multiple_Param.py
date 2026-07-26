from typing import Annotated

from fastapi import Body, FastAPI, Path, Query
from pydantic import BaseModel

app = FastAPI()


# -----------------------------
# Models
# -----------------------------
class Item(BaseModel):
    name: str
    price: float
    description: str | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


# =====================================================
# Example 1
# Path + Query + Single Body
# =====================================================
@app.put("/example1/items/{item_id}")
async def example1(
    item_id: Annotated[int, Path(ge=1)],
    q: Annotated[str | None, Query()] = None,
    item: Item | None = None,
):
    return {
        "item_id": item_id,
        "query": q,
        "item": item,
    }


# =====================================================
# Example 2
# Multiple Body Parameters
# =====================================================
@app.put("/example2/items/{item_id}")
async def example2(
    item_id: int,
    item: Item,
    user: User,
):
    return {
        "item_id": item_id,
        "item": item,
        "user": user,
    }


# =====================================================
# Example 3
# Multiple Body + Primitive Body Value
# =====================================================
@app.put("/example3/items/{item_id}")
async def example3(
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body(gt=0)],
):
    return {
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance,
    }


# =====================================================
# Example 4
# Path + Query + Multiple Body
# =====================================================
@app.put("/example4/items/{item_id}")
async def example4(
    item_id: Annotated[int, Path(ge=1)],
    item: Item,
    user: User,
    importance: Annotated[int, Body(gt=0)],
    q: Annotated[str | None, Query()] = None,
):
    return {
        "item_id": item_id,
        "query": q,
        "item": item,
        "user": user,
        "importance": importance,
    }


# =====================================================
# Example 5
# Embed=True
# =====================================================
@app.put("/example5/items/{item_id}")
async def example5(
    item_id: int,
    item: Annotated[Item, Body(embed=True)],
):
    return {
        "item_id": item_id,
        "item": item,
    }