from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from slowapi.extension import (
    _rate_limit_exceeded_handler,
)

app = FastAPI()

limiter = Limiter(
    key_func=get_remote_address
)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)


@app.post("/chat")
@limiter.limit("10/minute")
async def chat(request: Request):
    return {
        "answer": "Agent response"
    }