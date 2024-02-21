import string

from fastapi import Request
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy import select, delete
from database.models.items import ItemModel
from utils.db import get_db

templates = Jinja2Templates("public/views")

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

            return templates.TemplateResponse("menu.html", context=context)

    @staticmethod
    async def get_menu_popup(request: Request, item: str):
        async with await get_db() as db:
            items_query = await db.execute(select(ItemModel).where(ItemModel.name == item))
            item = items_query.scalar()

            html = f"""
                <div class="modal-dialog modal-lg modal-fullscreen-sm-down">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="itemWinTitle">Order an item</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            {item.name}
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-success">Purchase</button>
                        </div>
                    </div>
                </div>
            """

            return HTMLResponse(content=html)
