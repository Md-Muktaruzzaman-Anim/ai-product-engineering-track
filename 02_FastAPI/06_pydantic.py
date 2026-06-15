from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, validator, Field  # 1. Import necessary validation classes from Pydantic
from typing import Optional # 2. Import Optional typing for fields that aren't strictly required

app = FastAPI()

class Item(BaseModel): # 3. Create a data model inheriting from Pydantic's BaseModel
    name: str = Field(..., min_length=3) # 4. 'name' is required (ellipsis ...) and must be at least 3 characters long
    price: float = Field(..., ge=0) # 5. 'price' is required and must be greater than or equal to 0 (ge=0)
    description: Optional[str] = None # 6. An optional text field that defaults to None if omitted
    tax: float = 0.0 # 7. An optional numeric field that defaults to 0.0 if omitted

    @validator('tax') # 8. Set up a custom validator targeting the 'tax' field specifically
    def validate_tax(cls, v): # 9. 'v' represents the incoming tax value sent by the client
        if v is not None and v < 0: # 10. Check if the value is negative
            raise ValueError('Tax cannot be negative') # 11. Raise a clean custom error message
        return v # 12. Return the validated value if it passes the check
    

# A mock database dictionary to store items in memory
items = {"1": {"name": "Laptop", "price": 1000}}

@app.get("/items/{item_id}", status_code=status.HTTP_200_OK) # 13. Set the default successful response code to 200 OK
async def read_item(item_id: str):
    if item_id not in items: # 14. Check if the requested ID exists in our dictionary
        raise HTTPException( # 15. Interrupt execution to throw an explicit HTTP error exception
            status_code=404, # 16. Return a 404 Not Found status code
            detail="Item not found" # 17. Send a clear descriptive error message to the client
        )
    return items[item_id] # 18. Return the found item data if the ID exists