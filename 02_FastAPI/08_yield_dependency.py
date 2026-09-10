from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


class FakeDBSession:

    async def close(self):
        print("DB session closed")


async def get_db():
    db = FakeDBSession()

    print("DB session opened")

    try:
        yield db
    finally:
        await db.close()


@app.get("/users")
async def users(
    db: Annotated[FakeDBSession, Depends(get_db)]
):
    return {
        "message": "query database here",
    }