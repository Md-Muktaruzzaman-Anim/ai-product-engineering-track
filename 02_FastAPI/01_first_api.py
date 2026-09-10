from fastapi import FastAPI

app = FastAPI(
    title="Agent Backend",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "Agent backend is running",
    }


@app.get("/health")
async def health():
    return {"status": "alive"}