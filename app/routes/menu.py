from fastapi import APIRouter, Depends, Request, status, Form

from app.controllers.menu import MenuController

from app.dependecies.auth import SessionAuth

menuRouter = APIRouter(prefix="/menu", dependencies=[Depends(SessionAuth.validate_session)])

@menuRouter.get("/")
async def get_items(request: Request):
    return await MenuController.get_items(request)

@menuRouter.post("/add")
async def add_menu_item(request: Request, name: str = Form(None), price: float = Form(None)):
    return await MenuController.add_item(request, name, price)

@menuRouter.put("/update")
async def update_menu_item(request: Request, old_name: str = Form(None), name: str = Form(None), price: float = Form(None)):
    return await MenuController.modify_item(request, old_name, name, price)

@menuRouter.delete("/delete")
async def delete_menu_item(request: Request, item: str):
    return await MenuController.delete_item(request, item)

@menuRouter.get("/popup")
async def get_popup(request: Request, item: str):
    return await MenuController.get_modify_popup(request, item)