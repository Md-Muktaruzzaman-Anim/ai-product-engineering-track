from pydantic import BaseModel

class Product(BaseModel):
    id:int
    price:float

data = {
    "id": "101",
    "price": "499.99"
}

product = Product.model_validate(data)

print(product)
print(type(product.id))
print(type(product.price))