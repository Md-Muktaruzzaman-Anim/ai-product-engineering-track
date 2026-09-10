from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=5000,
    )
    thread_id: str = Field(
        min_length=1,
        max_length=100,
    )
    temperature: float = Field(
        default=0.7,
        ge=0,
        le=2,
    )


@app.post("/chat")
async def chat(request: ChatRequest):
    return {
        "message": request.message,
        "thread_id": request.thread_id,
        "temperature": request.temperature,
    }