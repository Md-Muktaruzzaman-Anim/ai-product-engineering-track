from fastapi import FastAPI, HTTPException

app = FastAPI()

agent_ready = True
database_ready = True


@app.get("/health")
async def health():
    return {
        "status": "alive"
    }


@app.get("/health/ready")
async def readiness():

    if not agent_ready:
        raise HTTPException(
            status_code=503,
            detail="Agent not ready",
        )

    if not database_ready:
        raise HTTPException(
            status_code=503,
            detail="Database not ready",
        )

    return {
        "status": "ready"
    }