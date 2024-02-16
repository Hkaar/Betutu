from typing import Any

from fastapi import Request, status
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware

from utils.config import Settings

templates = Jinja2Templates("public/views")

class HTTPIntercept(BaseHTTPMiddleware):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next, **kwargs):
        state = Settings.get_state("app", "status")

        if not state:
            context = {
                "request": request,

                "title": "403 | Forbidden",
                "msg": "Opps looks like were currently down! Please try again later!"
            }

            return templates.TemplateResponse("error.html", context=context, status_code=status.HTTP_403_FORBIDDEN)

        response = await call_next(request)

        if response.status_code == 404:
            context = {
                "request": request,

                "title": "404 | Not Found", 
                "msg": "Opps looks like the service you requested does not exist!"
            }

            return templates.TemplateResponse("error.html", context=context, status_code=status.HTTP_404_NOT_FOUND)

        return response
 