from typing import Annotated

from fastapi import FastAPI, Depends

app = FastAPI()


class CommonQueryParams:
    def __init__(self, q: str | None = None):
        self.q = q


@app.get("/")
async def home(
    params: Annotated[CommonQueryParams, Depends()]
):
    return {
        "query": params.q
    }