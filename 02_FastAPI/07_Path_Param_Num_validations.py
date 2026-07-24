from typing import Annotated

from fastapi import FastAPI, Path, Query

app = FastAPI(title="Path Validation Demo")


# --------------------------------------------------
# Fake Database
# --------------------------------------------------
products = {
    1: "Laptop",
    2: "Keyboard",
    3: "Mouse",
    4: "Monitor",
}


# --------------------------------------------------
# Example 1 : Normal Path Parameter
# --------------------------------------------------
@app.get("/normal/{product_id}")
async def normal(product_id: int):

    print("Function Executed!")

    return {
        "product_id": product_id
    }


# --------------------------------------------------
# Example 2 : Positive ID only
# --------------------------------------------------
@app.get("/products/{product_id}")
async def get_product(

    product_id: Annotated[
        int,
        Path(
            ge=1,
            title="Product ID",
            description="Must be greater than or equal to 1"
        )
    ]

):

    print("Validation Passed!")

    if product_id not in products:
        return {
            "message": "Product does not exist"
        }

    return {
        "id": product_id,
        "name": products[product_id]
    }


# --------------------------------------------------
# Example 3 : ID between 1 and 5
# --------------------------------------------------
@app.get("/limited/{product_id}")
async def limited(

    product_id: Annotated[
        int,
        Path(
            ge=1,
            le=5
        )
    ]

):

    return {
        "accepted_id": product_id
    }


# --------------------------------------------------
# Example 4 : gt and lt
# Must be >10 and <20
# --------------------------------------------------
@app.get("/range/{number}")
async def number_range(

    number: Annotated[
        int,
        Path(
            gt=10,
            lt=20
        )
    ]

):

    return {
        "number": number
    }


# --------------------------------------------------
# Example 5 : Path + Query together
# --------------------------------------------------
@app.get("/search/{user_id}")
async def search(

    user_id: Annotated[
        int,
        Path(ge=1)
    ],

    q: Annotated[
        str,
        Query(
            min_length=3,
            max_length=20
        )
    ]

):

    return {
        "user_id": user_id,
        "search": q
    }