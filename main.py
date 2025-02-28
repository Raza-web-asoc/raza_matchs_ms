from fastapi import FastAPI

from config.db import init_db
from router.router import match
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)
init_db()

instrumentator = Instrumentator(should_group_status_codes=False).instrument(app)
instrumentator.expose(app, endpoint="/metrics")

app.include_router(match)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Match API"}
