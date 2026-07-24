from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Response Model Tutorial")


# ======================================
# Request Model (Client -> Server)
# ======================================
class UserCreate(BaseModel):
    username: str
    email: str
    password: str


# ======================================
# Response Model (Server -> Client)
# ======================================
class UserResponse(BaseModel):
    id: int
    username: str
    email: str


# ======================================
# Fake Database
# ======================================
fake_db = []


# ======================================
# Path Parameter
# ======================================
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# ======================================
# Query Parameter
# ======================================
@app.get("/search")
async def search(skip: int = 0, limit: int = 10):
    return {
        "skip": skip,
        "limit": limit
    }


# ======================================
# Request Body + Response Model
# ======================================
@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):

    # Imagine this comes from database
    db_user = {
        "id": len(fake_db) + 1,
        "username": user.username,
        "email": user.email,
        "password": user.password,
        "is_admin": False
    }

    fake_db.append(db_user)

    return db_user


# ======================================
# Return All Users
# ======================================
@app.get("/users", response_model=list[UserResponse])
async def get_users():
    return fake_db