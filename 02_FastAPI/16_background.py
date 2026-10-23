from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def save_log(message: str):
    with open(
        "agent.log",
        "a",
        encoding="utf-8",
    ) as file:

        file.write(message + "\n")


@app.post("/chat")
async def chat(
    message: str,
    background_tasks: BackgroundTasks,
):

    background_tasks.add_task(
        save_log,
        message,
    )

    return {
        "answer": "Agent response"
    }