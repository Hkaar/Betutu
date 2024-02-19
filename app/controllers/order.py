from uuid import uuid4
from datetime import datetime

from fastapi import Request

from sqlalchemy import select, delete

from database.models.orders import OrderModel, OrderItemModel
from database.models.items import ItemModel

from utils.db import get_db

class OrderController:
    @staticmethod
    async def create(request: Request) -> str:
        token = uuid4().hex
        current = datetime.now()

        async with await get_db() as db:
            order = OrderModel(
                token=token,
                created=current
            )

            db.add(order)
            await db.commit()
            await db.refresh(order)

            return token

    @staticmethod
    async def delete(request: Request, token: str):
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
    async def add_item(request: Request):
        pass

    @staticmethod
    async def modify(request: Request):
        pass