import string

from fastapi import Request
from fastapi.templating import Jinja2Templates

from sqlalchemy import select, delete, insert, update
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
        
    @staticmethod
    async def get_modify_popup(request: Request, item: str):
        async with await get_db() as db:
            exist = await db.execute(select(ItemModel).where(ItemModel.name == item))

            if exist.scalar():
                context = {
                    "request": request,
                    "item": item
                }

                return templates.TemplateResponse("edit-menu.html", context=context)
        return False
        
    @staticmethod
    async def get_items(request: Request):
        async with await get_db() as db:
            items_query = await db.execute(select(ItemModel))
            items = [{"name": string.capwords(item[0].name), "price": item[0].price} for item in items_query.all()]

            context = {
                "request": request,
                "items": items
            }

            return templates.TemplateResponse("item.html", context=context)
        
    @staticmethod
    async def add_item(request: Request, name: str, price: float):
        async with await get_db() as db:
            exist = await db.execute(select(ItemModel).where(ItemModel.name == name))

            if not exist.scalar():
                await db.execute(insert(ItemModel).values({"name": name.lower(), "price": price}))
                await db.commit()

                return True 
        return False
    
    @staticmethod
    async def modify_item(request: Request, old_name: str, new_name: str, price: float):
        async with await get_db() as db:
            exist = await db.execute(select(ItemModel).where(ItemModel.name == old_name))

            if exist.scalar():
                await db.execute(update(ItemModel).values({"name": new_name, "price": price}).where(ItemModel.name == old_name))
                await db.commit()

                return True
        return False
        
    @staticmethod
    async def delete_item(request: Request, name: str):
        async with await get_db() as db:
            exists = await db.execute(select(ItemModel).where(ItemModel.name == name))
            exist = exists.scalar()

            if exist:
                await db.execute(delete(ItemModel).where(ItemModel.name == name))
                await db.commit()

                return True
        return False
