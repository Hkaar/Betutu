from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse, JSONResponse, Response

from app.controllers.user import UserController
from app.controllers.session import SessionController

from app.dependecies.auth import SessionAuth
from app.schemas.user import RegisterSchema, UserSchema

from utils.db import get_db

userRouter = APIRouter(prefix="/user")

@userRouter.get("/", dependencies=[Depends(SessionAuth.validate_session)])
async def home():
    return "Hello user"

@userRouter.get("/sign-in")
async def sign_in_page():
    pass

@userRouter.get("/register")
async def register_page():
    pass

@userRouter.post("/sign-in")
async def sign_in(user: UserSchema, request: Request):
    exist = await UserController.get(user.name, user.password)

    if exist:
        token = await SessionController.create(user.name, user.password, request)

        if not token:
            return Response(content="Failed to create session", status_code=status.HTTP_401_UNAUTHORIZED)
        
        response = Response(content="Successfully signed in!")
        response.set_cookie(
            key="sessionToken",
            value=token,
            httponly=True,
            samesite="strict",
        )

        return response
    
    return Response(content="Invalid credentials", status_code=status.HTTP_401_UNAUTHORIZED)

@userRouter.post("/register")
async def register(user: RegisterSchema, request: Request):
    created = await UserController.create(user.name, user.password)

    if created:
        token = await SessionController.create(user.name, user.password, request)

        if not token:
            return Response(content="Failed to create session", status_code=status.HTTP_401_UNAUTHORIZED)
        
        response = Response("Successfully registered!")
        response.set_cookie(
            key="sessionToken",
            value=token,
            httponly=True,
            samesite="strict",
        )

        return response
    
    return Response(content="Invalid credentials", status_code=status.HTTP_401_UNAUTHORIZED)

@userRouter.post("/sign-out")
async def sign_out(request: Request):
    token = request.cookies.get("sessionToken")

    await SessionController.delete(token)

    response = Response("Signed out successfully!")
    response.delete_cookie("sessionToken")
    
    return response
