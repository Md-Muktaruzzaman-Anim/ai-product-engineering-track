from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI(title="Query Validation Demo")


# =====================================================
# 1. Normal Query Parameter
# =====================================================
@app.get("/hello")
async def hello(name: str):

    return {
        "message": f"Hello {name}"
    }


# =====================================================
# 2. Optional Query Parameter
# =====================================================
@app.get("/search")
async def search(

    q: Annotated[
        str | None,
        Query()
    ] = None

):
    return {
        "query": q
    }


# =====================================================
# 3. Minimum Length
# =====================================================
@app.get("/search/min")
async def min_length(

    q: Annotated[
        str,
        Query(min_length=3)
    ]

):
    return {
        "query": q
    }


# =====================================================
# 4. Maximum Length
# =====================================================
@app.get("/search/max")
async def max_length(

    q: Annotated[
        str,
        Query(max_length=10)
    ]

):
    return {
        "query": q
    }


# =====================================================
# 5. Min + Max
# =====================================================
@app.get("/search/range")
async def range_validation(

    q: Annotated[
        str,
        Query(
            min_length=3,
            max_length=10
        )
    ]

):
    return {
        "query": q
    }


# =====================================================
# 6. Regex Pattern
# Must start with "chat-"
# =====================================================
@app.get("/chat")
async def chat(

    conversation: Annotated[
        str,
        Query(
            pattern="^chat-"
        )
    ]

):
    return {
        "conversation": conversation
    }


# =====================================================
# 7. Default Value
# =====================================================
@app.get("/default")
async def default_query(

    q: Annotated[
        str,
        Query(min_length=3)
    ] = "fastapi"

):
    return {
        "query": q
    }


# =====================================================
# 8. Alias
# URL:
# ?search-query=python
# =====================================================
@app.get("/alias")
async def alias(

    q: Annotated[
        str,
        Query(alias="search-query")
    ]

):
    return {
        "query": q
    }


# =====================================================
# 9. Multiple Query Values
# =====================================================
@app.get("/tags")
async def tags(

    q: Annotated[
        list[str] | None,
        Query()
    ] = None

):
    return {
        "received_tags": q
    }


# =====================================================
# 10. Documentation Metadata
# =====================================================
@app.get("/docs-example")
async def docs_example(

    q: Annotated[
        str,
        Query(
            min_length=3,
            max_length=20,
            title="Search Query",
            description="Type something to search."
        )
    ]

):
    return {
        "query": q
    }