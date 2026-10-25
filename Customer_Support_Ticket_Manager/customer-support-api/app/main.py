import logging
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Path,
    Query,
    Response,
    status,
)
from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app import models  # Register Ticket with Base.metadata
from app.models import Ticket
from app.schemas import (
    TicketCreate,
    TicketPriority,
    TicketResponse,
    TicketStatus,
    TicketUpdate,
)


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Learning-stage schema initialization.
    # Use Alembic migrations for production schema changes.
    Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(
    title="Customer Support API",
    description=(
        "REST API for creating, retrieving, updating, "
        "filtering, and deleting customer support tickets."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


# Root and health endpoints

@app.get("/")
def root():
    return {
        "message": "Customer Support API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

    except SQLAlchemyError as exc:
        logger.exception("Database health check failed.")

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed.",
        ) from exc

    return {
        "status": "ok",
        "database": "connected",
    }


# Create ticket

@app.post("/tickets", response_model=TicketResponse, status_code=status.HTTP_201_CREATED,)

def create_ticket(
    payload: TicketCreate,
    db: Annotated[Session, Depends(get_db)],
):
    ticket_data = payload.model_dump()
    ticket_data["email"] = str(payload.email)

    ticket = Ticket(**ticket_data)

    try:
        db.add(ticket)
        db.commit()
        db.refresh(ticket)

    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Could not create ticket.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create ticket.",
        ) from exc

    return ticket


# List and filter tickets

@app.get(
    "/tickets",
    response_model=list[TicketResponse],
)
def list_tickets(
    db: Annotated[Session, Depends(get_db)],
    status_filter: Annotated[
        TicketStatus | None,
        Query(alias="status"),
    ] = None,
    priority: TicketPriority | None = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    statement = select(Ticket)

    if status_filter is not None:
        statement = statement.where(
            Ticket.status == status_filter
        )

    if priority is not None:
        statement = statement.where(
            Ticket.priority == priority
        )

    statement = (
        statement
        .order_by(Ticket.ticket_id)
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(statement).all())


# Retrieve one ticket

@app.get(
    "/tickets/{ticket_id}",
    response_model=TicketResponse,
)
def get_ticket(
    ticket_id: Annotated[int, Path(ge=1)],
    db: Annotated[Session, Depends(get_db)],
):
    ticket = db.get(Ticket, ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found.",
        )

    return ticket


# Update ticket fields

@app.patch(
    "/tickets/{ticket_id}",
    response_model=TicketResponse,
)
def update_ticket(
    ticket_id: Annotated[int, Path(ge=1)],
    payload: TicketUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    ticket = db.get(Ticket, ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found.",
        )

    updates = payload.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide at least one field to update.",
        )

    for field, value in updates.items():
        if field == "email":
            value = str(value)

        setattr(ticket, field, value)

    try:
        db.commit()
        db.refresh(ticket)

    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Could not update ticket %s.", ticket_id)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not update ticket.",
        ) from exc

    return ticket


# Delete ticket

@app.delete(
    "/tickets/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_ticket(
    ticket_id: Annotated[int, Path(ge=1)],
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    ticket = db.get(Ticket, ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found.",
        )

    try:
        db.delete(ticket)
        db.commit()

    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Could not delete ticket %s.", ticket_id)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not delete ticket.",
        ) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)