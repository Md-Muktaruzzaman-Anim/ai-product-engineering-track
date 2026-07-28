from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()


def get_message():
    print("Resource Open")

    try:
        yield "Hello FastAPI"

    finally:
        print("Resource Closed")


@app.get("/")
def home(
    msg: Annotated[str, Depends(get_message)]
):
    return {"message": msg}