from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str
    thread_id: str


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    return {
        "answer": f"Agent received: {request.message}",
        "thread_id": "thread-123",
        # "secret": "this will not be exposed"
    }