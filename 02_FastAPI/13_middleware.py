import time

from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def request_timer(
    request: Request,
    call_next,
):

    start = time.perf_counter()

    response = await call_next(request)

    elapsed = (
        time.perf_counter() - start
    )

    response.headers["X-Response-Time"] = (
        f"{elapsed:.4f}s"
    )

    return response


@app.get("/")
async def root():
    return {
        "message": "hello"
    }