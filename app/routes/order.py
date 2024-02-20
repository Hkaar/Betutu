from fastapi import APIRouter, Depends, Request, status, Form

from app.controllers.order import OrderController

from app.dependecies.auth import SessionAuth

orderRouter = APIRouter(prefix="/order")

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
