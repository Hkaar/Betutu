from fastapi import APIRouter, Depends, Request, status, Form
from fastapi.responses import FileResponse, RedirectResponse

from app.controllers.order import OrderController

from app.dependecies.auth import SessionAuth

orderRouter = APIRouter(prefix="/order")

@orderRouter.get("/")
async def goto_order(request: Request):
    token = request.cookies.get("orderToken", None)

    if token:
        return FileResponse("public/views/menu.html")
    return RedirectResponse(url="/order/new")

@orderRouter.get("/new")
async def new_order(request: Request):
    token = await OrderController.create(request)

    response = RedirectResponse(url="/order")
    response.set_cookie("orderToken", token)

    return response

@orderRouter.get("/all/{type}")
async def get_all_orders(request: Request, type: str = None):
    match (type):
        case "items":
            return await OrderController.all_items(request)
        
        case _:
            return await OrderController.all_orders(request)
        
@orderRouter.get("/total")
async def total_price(request: Request):
    return await OrderController.total_price(request)

@orderRouter.post("/add")
async def fetch_orders():
    return await OrderController.get_item_price("Ayam Geprek")

@orderRouter.put("/update")
async def update_order():
    pass

@orderRouter.delete("/delete")
async def delete_order():
    pass
