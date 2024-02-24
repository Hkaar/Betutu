import string

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from sqlalchemy import select

from database.models.items import ItemModel

from utils.db import get_db

webRouter = APIRouter()

views = Jinja2Templates("public/views")

@webRouter.get("/")
async def home(request: Request):
    async with await get_db() as db:
        items_query = await db.execute(select(ItemModel))
        items = [{"name": string.capwords(item[0].name), "price": item[0].price, "img": item[0].img} for item in items_query.all()]

        context = {
            "request": request,
            "items": items
        }

        return views.TemplateResponse("index.html", context=context)