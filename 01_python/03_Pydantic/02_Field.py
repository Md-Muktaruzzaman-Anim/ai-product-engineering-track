# 1. default

from pydantic import BaseModel, Field

class User(BaseModel):
    country: str = Field(default="Bangladesh")

user = User()

print(user)

# 2. default_factory
from uuid import uuid4

id: str = Field(default_factory=lambda: str(uuid4()))

# 3. description

class price(BaseModel):
    price: float = Field(description="Price in USD")

# 4. examples

Field(
    examples=[19.99]
)

# 6. gt ge lt le

class validate(BaseModel):
    age: int = Field(ge=18)
    price: float = Field(gt=0)

# 7. min_length max_length

username: str = Field(
    min_length=3,
    max_length=20
)

# 8. pattern
# Formerly regex.

phone: str = Field(
    pattern=r"^\d{10}$" # Only 10 digits accepted.
)

# 10. exclude

# password should never appear.

password: str = Field(
    exclude=True
)

# Now model_dump() doesn't include it.