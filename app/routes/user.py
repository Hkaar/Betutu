from fastapi import APIRouter, Depends

from app.dependecies.auth import SessionAuth

userRouter = APIRouter(
    prefix="/user",
    dependencies=[Depends(SessionAuth.validate_session)]
)

@userRouter.get("/")
async def home():
    return "Hello user"
