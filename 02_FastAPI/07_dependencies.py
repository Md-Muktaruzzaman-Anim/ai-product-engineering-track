from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


def get_agent():
    return {
        "name": "demo-agent",
        "version": "1.0",
    }


def get_current_user():
    return {
        "id": "user-123",
        "name": "Muktar",
    }


@app.post("/chat")
async def chat(
    agent: Annotated[dict, Depends(get_agent)],
    user: Annotated[dict, Depends(get_current_user)],
):
    return {
        "user": user,
        "agent": agent,
    }