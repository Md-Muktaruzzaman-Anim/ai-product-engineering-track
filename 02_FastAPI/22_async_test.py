import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

app = FastAPI()


@app.get("/health")
async def health():
    return {
        "status": "alive"
    }


@pytest.mark.anyio
async def test_health():

    transport = ASGITransport(
        app=app
    )

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:

        response = await client.get(
            "/health"
        )

    assert response.status_code == 200

    assert response.json() == {
        "status": "alive"
    }