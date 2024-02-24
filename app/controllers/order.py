import string

from uuid import uuid4
from datetime import datetime

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy import select, delete, update, func

from database.models.orders import OrderModel, OrderItemModel
from database.models.items import ItemModel

from utils.db import get_db

views = Jinja2Templates("public/views")
templates = Jinja2Templates("public/templates")

class OrderController:
    @staticmethod
    async def get_order(request: Request):
        token = request.cookies.get("orderToken")

        async with await get_db() as db:
            status_query = await db.execute(select(OrderModel.status).where(OrderModel.token == token))
            order_status = status_query.scalar()

            if order_status and order_status != "pending":
                context = {
                    "request": request,
                    "token": token
                }

                response = views.TemplateResponse("completed.html", context=context)
                return response
            
            items_query = await db.execute(select(ItemModel))
            items = [{"name": string.capwords(item[0].name), "price": item[0].price, "img": item[0].img} for item in items_query.all()]

            context = {
                "request": request,
                "items": items
            }

            response = views.TemplateResponse("menu.html", context=context)

            exist = await db.execute(select(OrderModel.token).where(OrderModel.token == token))

            if not token or not exist.scalar():
                token = await OrderController.create(request)
                response.set_cookie("orderToken", token, httponly=True, samesite="strict")

            return response
        
    @staticmethod
    async def get_menu_popup(request: Request, item: str):
        async with await get_db() as db:
            items_query = await db.execute(select(ItemModel).where(ItemModel.name == item))
            item = items_query.scalar()

            context = {
                "request": request,
                "title": string.capwords(item.name),
                "price": item.price,
                "desc": item.desc,
                "img": item.img
            }

            return templates.TemplateResponse("menu-item.html", context=context)

    @staticmethod
    async def create(request: Request) -> str:
        token = uuid4().hex[:4]
        current = datetime.date(datetime.now())

        async with await get_db() as db:
            order = OrderModel(
                token=token,
                created=current,
                status="pending"
            )

            db.add(order)
            await db.commit()
            await db.refresh(order)

            return token 

    @staticmethod
    async def delete(request: Request, token: str):
        async with await get_db() as db:
            exist = await db.execute(select(OrderModel).where(OrderModel.token == token))

            if exist.scalar():
                await db.execute(delete(OrderModel).where(OrderModel.token == token))
                await db.commit()

                return True
        return False

    @staticmethod
    async def add_item(request: Request, item: str, amount: int):
        token = request.cookies.get("orderToken")

        async with await get_db() as db:
            order_query = await db.execute(select(OrderModel.id).where(OrderModel.token == token))
            order_id = order_query.scalar()

            if order_id:
                new_order = OrderItemModel(
                    order_id=order_id,
                    item=item.lower(),
                    amount=amount
                )

                db.add(new_order)
                await db.commit()
                await db.refresh(new_order)

                return JSONResponse(content={"msg": "Successfully added item"})
            
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opps looks like something wen wrong!"
        )

    @staticmethod
    async def get_item_price(item: str):
        async with await get_db() as db:
            item_query = await db.execute(select(ItemModel.price).where(
                (ItemModel.name == item)
            ))

            return item_query.scalar()
        
    @staticmethod
    async def all_items(request: Request):
        token = request.cookies.get("orderToken")
        items = []

        total_amount = 0

        async with await get_db() as db:
            order_query = await db.execute(select(OrderModel.id).where(OrderModel.token == token))
            order_id = order_query.scalar()

            order_items_query = await db.execute(select(OrderItemModel).where(OrderItemModel.order_id == order_id))
            order_items = [item[0] for item in order_items_query.all()]

            for order_item in order_items:
                item_name = string.capwords(order_item.item)
                amount = order_item.amount

                price = await OrderController.get_item_price(item_name.lower())
                total = price * amount

                total_amount += amount

                items.append({"id": order_item.id, "name": item_name, "total": total, "amount": amount})

            context = {
                "request": request,
                "items": items,
                "total_price": await OrderController.total_price(request),
                "total_amount": total_amount 
            }

            return templates.TemplateResponse("cart.html", context=context)
        
    @staticmethod
    async def all_orders(request: Request):
        orders = []

        async with await get_db() as db:
            order_query = await db.execute(select(OrderModel))
            order_ids = [order[0].id for order in order_query.all()]

            for order_id in order_ids:
                order_items_query = await db.execute(select(OrderItemModel).where(OrderItemModel.order_id == order_id))
                order_query = await db.execute(select(OrderModel).where(OrderModel.id == order_id))

                order_items = [item[0] for item in order_items_query.all()]
                order = order_query.scalar()
                
                total_amount = 0
                items = []

                for order_item in order_items:
                    item_name = string.capwords(order_item.item)
                    amount = order_item.amount

                    price = await OrderController.get_item_price(item_name.lower())
                    total = price * amount

                    total_amount += amount

                    items.append({
                        "name": item_name, 
                        "total": total, 
                        "amount": amount, 
                        "id": order_item.id
                    })

                orders.append({
                    "token": order.token,
                    "items": items,
                    "date": order.created,
                    "status": string.capwords(order.status),
                    "total_price": await OrderController.total_price(request, order.token)
                })
        
        context = {
            "request": request,
            "orders": orders
        }

        return templates.TemplateResponse("order-item.html", context=context)

    @staticmethod
    async def total_price(request: Request, token: str = None):
        if not token:
            token = request.cookies.get("orderToken")
        
        price = 0

        async with await get_db() as db:
            order_query = await db.execute(select(OrderModel.id).where(OrderModel.token == token))
            order_id = order_query.scalar()

            items_query = await db.execute(select(OrderItemModel).where(OrderItemModel.order_id == order_id))
            items = [item[0] for item in items_query.all()]

            for item in items:
                price_query = await db.execute(select(ItemModel.price).where(ItemModel.name == item.item.lower()))
                price += (price_query.scalar()*item.amount)
        
        return price
    
    @staticmethod
    async def total_orders(request: Request):
        async with await get_db() as db:
            orders_query = await db.execute(select(OrderModel))

            return len(orders_query.all())

    @staticmethod
    async def delete_item(request: Request, order_item_id: int):
        orderToken = request.cookies.get("orderToken")

        async with await get_db() as db:
            await db.execute(delete(OrderItemModel).where(OrderItemModel.id == order_item_id))
            await db.commit()

            return JSONResponse({"msg": "Successfully deleted!"})
        
    @staticmethod
    async def finish_order(request: Request):
        token = request.cookies.get("orderToken")

        async with await get_db() as db:
            exist = await db.execute(select(OrderModel).where(OrderModel.token == token))

            if exist.scalar():
                await db.execute(update(OrderModel).values({"status": "uncompleted"}).where(OrderModel.token == token))
                await db.commit()

                return JSONResponse({"msg": "Order was completed!"})
        
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opps looks like something went wrong!"
        )
    
    @staticmethod
    async def complete_order(request: Request, token: str):
        async with await get_db() as db:
            exist = await db.execute(select(OrderModel).where(OrderModel.token == token))

            if exist.scalar():
                await db.execute(update(OrderModel).values({"status": "completed"}).where(OrderModel.token == token))
                await db.commit()

                return JSONResponse({"msg": "Completed order"})
            
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opps looks like something went wrong!"
        )

    @staticmethod
    async def delete_all(request: Request):
        async with await get_db() as db:
            await db.execute(delete(OrderModel))
            await db.commit()

            return JSONResponse({"msg": "Deleted all orders!"})
        