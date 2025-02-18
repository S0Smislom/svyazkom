import os
import secrets
from random import choice, randint
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    correct_username = os.getenv("USERNAME", "").encode("utf-8")
    correct_password = os.getenv("PASSWORD", "").encode("utf-8")

    if not correct_username or not correct_username:
        return

    if not (
        secrets.compare_digest(credentials.username.encode("utf-8"), correct_username)
        and secrets.compare_digest(
            credentials.password.encode("utf-8"), correct_password
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/", response_model=List[dict], tags=["locations"])
async def get_locations(_: str = Depends(authenticate_user)) -> List[dict]:
    location_generators = [
        _get_location_v1,
        _get_location_v2,
        _get_location_v3,
        _get_location_v4,
    ]
    return [
        _generate_random_location(location_generators)
        for _ in range(randint(1, 50_000))
    ]


def _generate_random_location(generators: List) -> dict:
    return choice(generators)()


def _get_location_v1() -> dict:
    return {"lac": randint(1, 1_000_000)}


def _get_location_v2() -> dict:
    return {"eci": randint(1, 1_000_000)}


def _get_location_v3() -> dict:
    return {
        "lac": randint(1, 1_000_000),
        "cellid": randint(1, 1_000_000),
    }


def _get_location_v4() -> dict:
    return {
        "lac": randint(1, 1_000_000),
        "cellid": randint(1, 1_000_000),
        "eci": randint(1, 1_000_000),
    }
