from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/health")
async def health():
    return {
        "status": "alive"
    }


@app.post("/chat")
async def chat(message: dict):
    return {
        "answer": (
            f"Processed: "
            f"{message['text']}"
        )
    }


client = TestClient(app)


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "alive"
    }


def test_chat():

    response = client.post(
        "/chat",
        json={"text": "hello"},
    )

    assert response.status_code == 200

    assert (
        "answer"
        in response.json()
    )