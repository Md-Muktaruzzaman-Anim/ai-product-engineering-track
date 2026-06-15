from fastapi import FastAPI
from pydantic import BaseModel

# 1. Define the data structure (Schema)
class Item(BaseModel):
    name: str
    price: float

# 2. Initialize the FastAPI application
app = FastAPI()

# 3. READ Operation (GET Method)
@app.get("/items/{item_id}") 
def read_item(item_id: int):
    return {"item_id": item_id}

# 4. CREATE Operation (POST Method)
@app.post("/items/") 
def create_item(item: Item): 
    return {"name": item.name, "price": item.price} 

# 5. UPDATE Operation (PUT Method)
@app.put("/items/{item_id}") 
def update_item(item_id: int, item: Item): 
    return {"item_id": item_id, "name": item.name, "price": item.price} 

# 6. DELETE Operation (DELETE Method)
@app.delete("/items/{item_id}") 
def delete_item(item_id: int): 
    return {"message": f"Item with id {item_id} has been deleted"} 