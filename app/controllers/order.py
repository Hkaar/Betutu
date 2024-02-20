from uuid import uuid4
from datetime import datetime

from fastapi import Request
from fastapi.responses import JSONResponse

from sqlalchemy import select, delete

from database.models.orders import OrderModel, OrderItemModel
from database.models.items import ItemModel

from app.schemas.item import ItemOrderSchema

from utils.db import get_db

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
    async def add_item(request: Request, item_data: ItemOrderSchema):
        token = request.cookies.get("orderToken")

        async with await get_db() as db:
            order_query = await db.execute(select(OrderModel.id).where(
                (OrderModel.token == token)
            ))

            order_id = order_query.scalar()

            if order_id:
                new_order = OrderItemModel(
                    order_id=order_query.scalar(),
                    item=item_data.name.lower(),
                    amount=item_data.amount
                )

                db.add(new_order)
                await db.commit()
                await db.refresh(new_order)

                return True
        return False

    @staticmethod
    async def modify(request: Request):
        token = request.cookies.get("orderToken")

        async with await get_db() as db:
            pass

    @staticmethod
    async def all_items(request: Request):
        token = request.cookies.get("orderToken")

        async with await get_db() as db:
            order_query = await db.execute(select(OrderModel.id).where(OrderModel.token == token))
            order_id = order_query.scalar()

            items_query = await db.execute(select(OrderItemModel).where(OrderItemModel.order_id == order_id))
            items = {item[0].item : item[0].amount for item in items_query.all()}

            return items
        
    @staticmethod
    async def get_item_price(item):
        async with await get_db() as db:
            item_query = await db.execute(select(ItemModel.price).where(
                (ItemModel.name == item)
            ))

            return item_query.scalar()
        
    @staticmethod
    async def all_orders(request: Request):
        result = {}

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