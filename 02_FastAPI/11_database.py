from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


DATABASE_URL = (
    "postgresql+asyncpg://postgres:password@localhost/agent_db"
)


class Base(DeclarativeBase):
    pass


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    title: Mapped[str] = mapped_column(
        String(200)
    )


engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def get_db():
    async with SessionLocal() as session:
        yield session


app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as connection:
        await connection.run_sync(
            Base.metadata.create_all
        )


@app.post("/conversations")
async def create_conversation(
    title: str,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    conversation = Conversation(
        title=title
    )

    db.add(conversation)

    await db.commit()
    await db.refresh(conversation)

    return {
        "id": conversation.id,
        "title": conversation.title,
    }


@app.get("/conversations")
async def list_conversations(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(
        select(Conversation)
    )

    conversations = result.scalars().all()

    return [
        {
            "id": item.id,
            "title": item.title,
        }
        for item in conversations
    ]
