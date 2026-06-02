from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.models  # noqa: F401 — registers all models with SQLModel.metadata
from app.api.routers import films, people, planets, species, starships, vehicles
from app.config import APP_NAME
from app.db import create_db_and_tables


@asynccontextmanager
async def lifespan(_app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title=APP_NAME, version="1.0.0", lifespan=lifespan)

for module in (people, films, planets, species, vehicles, starships):
    app.include_router(module.router)
