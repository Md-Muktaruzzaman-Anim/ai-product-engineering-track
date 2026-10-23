from fastapi import (
    Depends,
    FastAPI,
)
from fastapi.testclient import TestClient

app = FastAPI()


def get_agent():
    return "real-agent"


@app.get("/run")
async def run(
    agent=Depends(get_agent),
):
    return {
        "agent": agent
    }


def fake_agent():
    return "fake-agent"


app.dependency_overrides[
    get_agent
] = fake_agent


client = TestClient(app)


def test_run():

    response = client.get("/run")

    assert response.status_code == 200

    assert response.json() == {
        "agent": "fake-agent"
    }