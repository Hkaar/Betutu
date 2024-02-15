from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.middleware.http import HTTPIntercept
from app.middleware.auth import SessionAuth

from utils.config import Settings

from utils.db import DBManager
from utils.redis import RedisManager

APP_NAME = Settings.get_env("APP_NAME")
APP_VERSION = Settings.get_env("APP_VERSION")

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)

app.add_middleware(HTTPIntercept)
app.add_middleware(SessionAuth)

app.mount("/src", StaticFiles(directory="public"), name="src")

@app.on_event("startup")
async def init():
    await DBManager.init()
    await RedisManager.connect()

@app.on_event("shutdown")
async def shutdown():
    await DBManager.shutdown()
    await RedisManager.disconnect()

@app.get("/")
def home():
    return "hello"