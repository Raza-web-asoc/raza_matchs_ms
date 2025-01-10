from fastapi import FastAPI

from config.db import init_db
from router.router import match
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"]
)
init_db()

app.include_router(match)
