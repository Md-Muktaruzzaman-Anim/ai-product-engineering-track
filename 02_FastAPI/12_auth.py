from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
)
from jwt.exceptions import InvalidTokenError

app = FastAPI()

SECRET_KEY = "change-this-in-production"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token"
)


def create_access_token(
    user_id: str, expires_minutes: int = 30,) -> str:

    expire = (
        datetime.now(timezone.utc)
        + timedelta(minutes=expires_minutes)
    )

    payload = {
        "sub": user_id,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


@app.post("/token")
async def login():

    # Demo only.
    # Real project:
    # verify username/password against PostgreSQL.

    token = create_access_token(
        user_id="user-123"
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], ):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        return {
            "id": user_id
        }

    except InvalidTokenError:
        raise credentials_exception


@app.get("/me")
async def me(
    user=Depends(get_current_user),
):
    return user