from fastapi import APIRouter, Depends, Request, status, Form
from fastapi.responses import RedirectResponse, JSONResponse, Response, FileResponse

from app.controllers.user import UserController
from app.controllers.session import SessionController

from app.dependecies.auth import SessionAuth
from app.schemas.user import RegisterSchema, UserSchema

userRouter = APIRouter(prefix="/user")

@userRouter.get("/home", dependencies=[Depends(SessionAuth.validate_session)])
async def home():
    return FileResponse("public/views/dashboard.html")

@userRouter.get("/sign-in")
async def sign_in_page():
    return FileResponse("public/views/user-login.html")

@userRouter.get("/register")
async def register_page():
    return FileResponse("public/views/user-register.html")

@userRouter.post("/sign-in")
async def sign_in(request: Request, username: str = Form(None), password: str = Form(None)):
    exist = await UserController.get(username, password)

    if exist:
        token = await SessionController.create(username, password, request)

        if not token:
            return Response(content="Failed to create session", status_code=status.HTTP_401_UNAUTHORIZED)
        
        response = RedirectResponse(url="/user/home", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(
            key="sessionToken",
            value=token,
            httponly=True,
            samesite="strict",
        )

        return response
    
    return RedirectResponse(url="/error/401", status_code=status.HTTP_303_SEE_OTHER)

@userRouter.post("/register")
async def register(request: Request, username: str = Form(None), password: str = Form(None)):
    created = await UserController.create(username, password)

    if created:
        token = await SessionController.create(username, password, request)

        if not token:
            return Response(content="Failed to create session", status_code=status.HTTP_401_UNAUTHORIZED)
        
        response = RedirectResponse(url="/user/home", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(
            key="sessionToken",
            value=token,
            httponly=True,
            samesite="strict",
        )

        return response
    
    return RedirectResponse(url="/error/401", status_code=status.HTTP_303_SEE_OTHER)

@userRouter.post("/sign-out")
async def sign_out(request: Request):
    token = request.cookies.get("sessionToken")

    await SessionController.delete(token)

    response = RedirectResponse(url="/user/sign-in", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("sessionToken")
    
    return response
