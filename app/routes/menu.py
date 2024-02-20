from fastapi import APIRouter, Depends, Request, status, Form

from app.dependecies.auth import SessionAuth

menuRouter = APIRouter(prefix="/order", dependencies=[Depends(SessionAuth.validate_session)])

@menuRouter.post("/menu/add")
async def add_menu_item():
    pass

@menuRouter.put("/menu/update")
async def update_menu_item():
    pass

@menuRouter.delete("/menu/delete")
async def delete_menu_item():
    pass