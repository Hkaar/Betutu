from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.middleware.http import HTTPIntercept
from app.routes import userRouter, webRouter, orderRouter, menuRouter

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

app.mount("/public", StaticFiles(directory="public"), name="public")

app.include_router(userRouter)
app.include_router(webRouter)
app.include_router(orderRouter)
app.include_router(menuRouter)

templates = Jinja2Templates("public/views")

@app.on_event("startup")
async def init():
    await DBManager.init()
    await RedisManager.connect()

@app.on_event("shutdown")
async def shutdown():
    await DBManager.shutdown()
    await RedisManager.disconnect()

@app.get("/error/{code}")
def error_handle(code: int, request: Request):
    match (code):
        case 401:
            context = {
                "request": request,
                "title": "401 | Unauthorized",
                "msg": "Opps looks like you're not authorized! Please try again!"
            }
        
            return templates.TemplateResponse(
                "error.html", context=context, status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        case 408:
            context = {
                "request": request,
                "title": "408 | Request Timeout",
                "msg": "Looks like something went wrong! Try again in a few moments!"
            }

            return templates.TemplateResponse(
                "error.html", context=context, status_code=status.HTTP_408_REQUEST_TIMEOUT
            )