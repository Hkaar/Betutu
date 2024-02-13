from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.middleware.http import HTTPIntercept

from utils.config import Settings

from utils.db import DBManager, engine
from utils.redis import RedisManager

APP_NAME = Settings.get_env("APP_NAME")
APP_VERSION = Settings.get_env("APP_VERSION")

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)

app.add_middleware(HTTPIntercept)

app.mount("/public", StaticFiles(directory="public"), name="src")

db_manager = DBManager(engine)

@app.on_event("startup")
async def init():
    await db_manager.create_tables()
    await RedisManager.connect()

@app.on_event("shutdown")
async def shutdown():
    await db_manager.shutdown()
    await RedisManager.disconnect()