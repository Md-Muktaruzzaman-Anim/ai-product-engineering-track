import asyncio
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI

app = FastAPI()

executor = ThreadPoolExecutor(max_workers=4)


def blocking_work(value: int) -> int:
    total = 0

    for number in range(5_000_000):
        total += number * value

    return total


@app.get("/compute")
async def compute(value: int = 2):

    loop = asyncio.get_running_loop()

    result = await loop.run_in_executor(
        executor,
        blocking_work,
        value,
    )

    return {
        "result": result,
    }