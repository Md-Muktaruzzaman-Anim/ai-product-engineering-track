from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items")
async def get_items(
    token: Annotated[str, Depends(oauth2_scheme)]
):
    return {
        "received_token": token
    }