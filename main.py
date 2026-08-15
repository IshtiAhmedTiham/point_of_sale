from dotenv import load_dotenv
load_dotenv()

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from src.routers.v1.router import router
from src.config.database import init_db


@asynccontextmanager
async def lifespan(app : FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
add_pagination(app)

app.include_router(router, prefix="/api/v1")