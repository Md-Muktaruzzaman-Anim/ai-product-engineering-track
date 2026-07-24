from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, HttpUrl

app = FastAPI(title="Nested Models Demo")

# -------------------------
# Nested Models
# -------------------------

class Seller(BaseModel):
    name: str
    email: str


class Image(BaseModel):
    url: HttpUrl
    title: str


class Product(BaseModel):
    id: int
    name: str
    price: float
    seller: Seller
    images: list[Image]


# Fake Database
products = {}


# -------------------------
# Create Product
# -------------------------

@app.post("/products", response_model=Product)
async def create_product(product: Product):

    if product.id in products:
        raise HTTPException(
            status_code=400,
            detail="Product ID already exists"
        )

    products[product.id] = product

    return product


# -------------------------
# Get Product
# -------------------------

@app.get("/products/{product_id}", response_model=Product)
async def get_product(
    product_id: Annotated[
        int,
        Path(ge=1)
    ]
):

    if product_id not in products:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return products[product_id]


# -------------------------
# Search Products
# -------------------------

@app.get("/search")
async def search_products(
    keyword: Annotated[
        str,
        Query(min_length=3, max_length=20)
    ]
):

    result = []

    for product in products.values():
        if keyword.lower() in product.name.lower():
            result.append(product)

    return result