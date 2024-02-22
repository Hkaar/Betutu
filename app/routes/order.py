from fastapi import APIRouter, Depends, Request, status, Form
from fastapi.responses import RedirectResponse

from app.controllers.order import OrderController

from app.dependecies.auth import SessionAuth

orderRouter = APIRouter(prefix="/order")

@orderRouter.get("/")
async def goto_order(request: Request):
    return await OrderController.get_order(request)

@orderRouter.get("/menu-item/{item}")
async def get_menu_item(request: Request, item: str):
    return await OrderController.get_menu_popup(request, item)

@orderRouter.get("/orders")
async def get_order_items(request: Request):
    return await OrderController.all_items(request)

@orderRouter.get("/all")
async def get_all_orders(request: Request):
    return await OrderController.all_orders(request)

@orderRouter.post("/add")
async def add_order_item(request: Request, item: str = Form(None), amount: int = Form(None)):
    await OrderController.add_item(request, item, amount)

# @orderRouter.put("/update", dependencies=[Depends(SessionAuth.validate_session)])
# async def update_order():
#     pass

@orderRouter.delete("/delete", dependencies=[Depends(SessionAuth.validate_session)])
async def delete_order(request: Request, token: str):
    return await OrderController.delete(request, token)

@orderRouter.delete("/delete/item")
async def delete_order_item(request: Request, id: int):
    await OrderController.delete_item(request, id)

@orderRouter.put("/complete")
async def complete_page(request: Request):
    return await OrderController.finish_order(request)