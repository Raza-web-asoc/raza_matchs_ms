from fastapi import FastAPI
from router.router import match

app = FastAPI()

app.include_router(match)