from contextlib import asynccontextmanager

from fastapi import FastAPI


resources = {}


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Starting application...")

    resources["agent"] = "compiled-agent"
    resources["db"] = "database-pool"

    yield

    print("Stopping application...")

    resources.clear()


app = FastAPI(
    lifespan=lifespan
)


@app.get("/health")
async def health():
    return {
        "status": "alive",
        "resources": list(resources),
    }