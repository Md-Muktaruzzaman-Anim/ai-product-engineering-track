from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class AgentConfig(BaseModel):
    model: str
    temperature: float = Field(
        default=0.7,
        ge=0,
        le=2,
    )


class ChatRequest(BaseModel):
    message: str
    thread_id: str
    config: AgentConfig


@app.post("/chat")
async def chat(request: ChatRequest):
    return {
        "message": request.message,
        "thread_id": request.thread_id,
        "model": request.config.model,
        "temperature": request.config.temperature,
    }