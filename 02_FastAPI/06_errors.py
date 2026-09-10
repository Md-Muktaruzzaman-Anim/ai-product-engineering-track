from fastapi import FastAPI, HTTPException

app = FastAPI()


fake_threads = {
    "abc": {
        "id": "abc",
        "name": "AI Research",
    }
}


@app.get("/threads/{thread_id}")
async def get_thread(thread_id: str):

    thread = fake_threads.get(thread_id)

    if thread is None:
        raise HTTPException(
            status_code=404,
            detail="Thread not found",
        )

    return thread