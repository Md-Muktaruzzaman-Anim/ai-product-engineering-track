from pydantic import BaseModel, Field

class Item(BaseModel):

    name: str

    description: str | None = Field(
        default=None,
        max_length=300
    )

    price: float = Field(
        gt=0
    )

    tax: float | None = None