from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# Fake Database
products = {
    1: {"name": "Laptop", "price": 1200},
    2: {"name": "Mouse", "price": 25},
}


class Product(BaseModel):
    name: str
    price: float


# -------------------------
# Normal Success
# -------------------------
@app.get("/")
async def home():
    return {"message": "Everything is working!"}


# -------------------------
# Error Handling Example 1
# -------------------------
@app.get("/products/{product_id}")
async def get_product(product_id: int):

    print("1. Request received")

    if product_id not in products:
        print("2. Product not found")
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    print("3. Product found")

    return products[product_id]


# -------------------------
# Error Handling Example 2
# -------------------------
@app.post("/products")
async def create_product(product: Product):

    print("1. Request received")

    # Check duplicate product
    for p in products.values():
        if p["name"].lower() == product.name.lower():
            print("2. Duplicate product")
            raise HTTPException(
                status_code=400,
                detail="Product already exists"
            )

    print("3. Creating product")

    new_id = max(products.keys()) + 1

    products[new_id] = {
        "name": product.name,
        "price": product.price,
    }

    print("4. Product created")

    return {
        "id": new_id,
        "product": products[new_id]
    }


# -------------------------
# raise vs return
# -------------------------
@app.get("/demo")
async def demo():

    print("Start")

    raise HTTPException(
        status_code=400,
        detail="Something went wrong"
    )

    print("This line never runs")

    return {"message": "Success"}