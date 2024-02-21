import string

from fastapi import Request
from fastapi.templating import Jinja2Templates

from sqlalchemy import select, delete
from database.models.items import ItemModel
from utils.db import get_db

views = Jinja2Templates("public/views")
templates = Jinja2Templates("public/templates")

class MenuController:
    @staticmethod
    async def get_menu(request: Request):
        html = []

        async with await get_db() as db:
            items_query = await db.execute(select(ItemModel))
            items = {string.capwords(item[0].name) : item[0].price for item in items_query.all()}

            context = {
                "request": request,
                "items": items
            }

            return views.TemplateResponse("menu.html", context=context)

    @staticmethod
    async def get_menu_popup(request: Request, item: str):
        async with await get_db() as db:
            items_query = await db.execute(select(ItemModel).where(ItemModel.name == item))
            item = items_query.scalar()

            context = {
                "request": request,
                "title": string.capwords(item.name),
                "price": item.price,
                "desc": "Just no"
            }

            return templates.TemplateResponse("menu-item.html", context=context)