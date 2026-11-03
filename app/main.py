from dotenv import load_dotenv
load_dotenv()

from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.src.routers.v1.router import router
from app.src.config.database import init_db


@asynccontextmanager
async def lifespan(app : FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

add_pagination(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")