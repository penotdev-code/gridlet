"""Gridlet API entrypoint."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models  # noqa: F401 — register models on Base.metadata
from .config import settings
from .database import Base, engine
from .routers import auth, favorites, lists


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Dev convenience: create tables on startup. In production, use Alembic
    # migrations instead (see alembic/ and the README).
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Gridlet API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(lists.router)
app.include_router(favorites.router)


@app.get("/health", tags=["meta"])
async def health() -> dict:
    return {"status": "ok"}
