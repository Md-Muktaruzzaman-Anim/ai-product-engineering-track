# model_dump() & model_dump_json()

# This is the method you'll use constantly.

from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

user = User(
    name="Alice",
    age=25
)

print(user.model_dump())
print(user.model_dump_json())

# include

