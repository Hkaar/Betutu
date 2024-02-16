from fastapi import APIRouter

webRouter = APIRouter()

@webRouter.get("/")
def home():
    return "My landing page"