from fastapi import APIRouter, Request
from fastapi.responses import FileResponse

webRouter = APIRouter()

@webRouter.get("/")
def home():
    return FileResponse("public/views/index.html")