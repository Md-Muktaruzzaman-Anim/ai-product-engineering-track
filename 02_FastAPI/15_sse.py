import asyncio
from collections.abc import AsyncIterable

from fastapi import FastAPI
from fastapi.sse import (
    EventSourceResponse,
    ServerSentEvent,
)
from pydantic import BaseModel

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.post("/chat/stream", response_class=EventSourceResponse,)

async def chat_stream(request: ChatRequest,) -> AsyncIterable[ServerSentEvent]:

    words = request.message.split()

    for word in words:

        await asyncio.sleep(0.5)

        yield ServerSentEvent(
            data=word,
            event="token",
        )

    yield ServerSentEvent(
        raw_data="[DONE]",
        event="done",
    )