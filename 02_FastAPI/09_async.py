import asyncio

from fastapi import FastAPI

app = FastAPI()


async def call_llm():
    await asyncio.sleep(2)
    return "LLM response"


async def call_tool():
    await asyncio.sleep(2)
    return "Tool response"


@app.get("/sequential")
async def sequential():

    llm = await call_llm()
    tool = await call_tool()

    return {
        "llm": llm,
        "tool": tool,
    }


@app.get("/parallel")
async def parallel():

    llm, tool = await asyncio.gather(
        call_llm(),
        call_tool(),
    )

    return {
        "llm": llm,
        "tool": tool,
    }