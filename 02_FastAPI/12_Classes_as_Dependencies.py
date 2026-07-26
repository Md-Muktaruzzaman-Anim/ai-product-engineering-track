from fastapi import FastAPI, Depends

app = FastAPI()


class CommonParams:

    def __init__(
        self,
        name: str = "",
        page: int = 1,
        limit: int = 10,
    ):
        self.name = name
        self.page = page
        self.limit = limit


@app.get("/users")
def get_users(
    commons: CommonParams = Depends(),
):
    return {
        "name": commons.name,
        "page": commons.page,
        "limit": commons.limit,
    }