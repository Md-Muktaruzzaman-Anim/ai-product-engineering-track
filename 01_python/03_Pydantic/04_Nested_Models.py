'''Step 1 — Create the Small Object

Instead of thinking about User,

think about Address first.'''

from pydantic import BaseModel

class Address(BaseModel):
    city: str
    street: str
    zip_code: str

# Step 2 — Put It Inside Another Model

class User(BaseModel):
    name: str
    age: int
    address: Address

'''Look carefully. 

    address: Address
    NOT
    address: dict
    NOT
    address: str

We're saying, "The address field must itself be an Address object."'''

"""
User

name
age
address

        │

        ▼

Address

city
street
zip_code
"""

address = Address(
    city="Dhaka",
    street="Road 10",
    zip_code="1207"
)

user = User(
    name="Alice",
    age=25,
    address=address
)

print(user)
print(type(user.address))