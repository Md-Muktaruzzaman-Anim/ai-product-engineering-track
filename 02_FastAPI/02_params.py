from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/threads/{thread_id}")
async def get_thread(thread_id: str):
    return {
        "thread_id": thread_id,
    }


@app.get("/threads")
async def list_threads(
    limit: int = 20,
    offset: int = 0,
):
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 100",
        )

    return {
        "limit": limit,
        "offset": offset,
    }


@app.post("/chat")
async def chat():
    return {
        "message": "agent would run here",
    }


@app.put("/threads/{thread_id}")
async def update_thread(thread_id: str):
    return {
        "updated": thread_id,
    }


@app.delete("/threads/{thread_id}")
async def delete_thread(thread_id: str):
    return {
        "deleted": thread_id,
    }