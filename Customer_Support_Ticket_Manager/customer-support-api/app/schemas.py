from datetime import datetime
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


TicketStatus = Literal[
    "open",
    "in_progress",
    "resolved",
    "closed",
]

TicketPriority = Literal[
    "low",
    "medium",
    "high",
]


class TicketCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    subject: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    priority: TicketPriority = "medium"

    @field_validator("customer_name", "subject", "description")
    @classmethod
    def validate_non_empty_text(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("This field cannot be empty.")

        return value


class TicketUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    email: EmailStr | None = None
    subject: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )
    description: str | None = Field(
        default=None,
        min_length=1,
    )
    status: TicketStatus | None = None
    priority: TicketPriority | None = None

    @field_validator("customer_name", "subject", "description")
    @classmethod
    def validate_optional_text(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError("This field cannot be empty.")

        return value


class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ticket_id: int
    customer_name: str
    email: EmailStr
    subject: str
    description: str
    status: TicketStatus
    priority: TicketPriority
    created_at: datetime