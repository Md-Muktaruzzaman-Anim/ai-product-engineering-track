from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()


def get_name():
    return "Sakib"


def greet(
    name: Annotated[str, Depends(get_name)]
):
    return f"Hello {name}"


@app.get("/")
def home(
    message: Annotated[str, Depends(greet)]
):
    return {"message": message}