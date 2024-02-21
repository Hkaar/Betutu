import string

from uuid import uuid4
from datetime import datetime

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy import select, delete

from database.models.orders import OrderModel, OrderItemModel
from database.models.items import ItemModel

from utils.db import get_db

templates = Jinja2Templates("public/templates")

class OrderController:
    @staticmethod
    async def create(request: Request) -> str:
        token = uuid4().hex
        current = datetime.now()

        async with await get_db() as db:
            order = OrderModel(
                token=token,
                created=current,
                status=False
            )

            db.add(order)
            await db.commit()
            await db.refresh(order)

            return token 

    @staticmethod
    async def delete(request: Request):
        token = request.cookies.get("orderToken")

        async with await get_db() as db:
            exist = await db.execute(select(OrderModel).where(
                (OrderModel.token == token)
            ))

            if exist.scalar():
                await db.execute(delete(OrderModel).where(
                    OrderModel.token == token
                ))

                return True
        return False

    @staticmethod
    async def add_item(request: Request, item: str, amount: int):
        token = request.cookies.get("orderToken")

        async with await get_db() as db:
            order_query = await db.execute(select(OrderModel.id).where(
                (OrderModel.token == token)
            ))

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

                return JSONResponse(content={"msg": "Successfully added item"}, headers={"Location": "/order"})
            
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opps looks like something wen wrong!"
        )

    @staticmethod
    async def modify(request: Request):
        token = request.cookies.get("orderToken")

        async with await get_db() as db:
            pass
        
    @staticmethod
    async def get_item_price(item):
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
                item_name = order_item.item
                amount = order_item.amount

                price = await OrderController.get_item_price(item_name.lower())
                total = price * amount

                total_amount += amount

                items.append({"id": order_item.id, "name": string.capwords(item_name), "total": total, "amount": amount})

            context = {
                "request": request,
                "items": items,
                "total_price": await OrderController.total_price(request),
                "total_amount": total_amount 
            }

            return templates.TemplateResponse("cart.html", context=context)
        
    @staticmethod
    async def all_orders(request: Request):
        result = {}
        html = []

        async with await get_db() as db:
            order_query = await db.execute(select(OrderModel))
            order_ids = [order[0].id for order in order_query.all()]

            for order_id in order_ids:
                order_items_query = await db.execute(select(OrderItemModel).where(OrderItemModel.order_id == order_id))
                order_token_query = await db.execute(select(OrderModel.token).where(OrderModel.id == order_id))

                order_items = [item[0] for item in order_items_query.all()]
                items = []

                for item in order_items:
                    item_name = item.item
                    amount = item.amount

                    price = await OrderController.get_item_price(item_name.lower())
                    total = price * amount

                    items.append({"name": item_name, "total": total, "amount": amount})

                result[order_token_query.scalar()] = items

            for order in result:
                pass

        return result

    @staticmethod
    async def total_price(request: Request):
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
    async def delete_item(request: Request, order_item_id: int):
        token = request.cookies.get("orderToken")

        if not token:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Opps looks like something wen wrong!"
            )

        async with await get_db() as db:
            await db.execute(delete(OrderItemModel).where(OrderItemModel.id == order_item_id))
            await db.commit()

            return JSONResponse({"msg": "Successfully deleted!"})
        