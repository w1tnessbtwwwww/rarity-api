from contextlib import asynccontextmanager
from typing import Union

from alembic import command
from alembic.config import Config
from fastapi import FastAPI

app = FastAPI()


@asynccontextmanager
async def lifespan():
    run_migrations()
    yield


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
