from typing import Any, Callable, Awaitable

from datetime import datetime, timedelta

from fastapi import Request, status
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.sessions import SessionModel

from utils.db import get_db

templates = Jinja2Templates("public/views")

class SessionAuth(BaseHTTPMiddleware):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app)

    async def clear_sessions(self):
        current = datetime.utcnow()
        expire = current - timedelta(days=1)
        
        async with await get_db() as db:
            await db.execute(delete(SessionModel).where(
                SessionModel.created < expire
            ))
            await db.commit()

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]):
        await self.clear_sessions()

        token = request.cookies.get("sessionToken", "")
        user_agent = request.headers.get("user-agent", "")

        async with await get_db() as db:
            exist = await db.execute(select(SessionModel).where(
                (SessionModel.token == token) & (SessionModel.user_agent == user_agent) 
            ))

            if exist.scalar():
                response = await call_next(request)
                return response
            
            context = {
                "request": request,

                "title": "401 | Unauthorized",
                "msg": "Opps looks like your unauthorized please try again later!"
            }
        
        return templates.TemplateResponse("error.html", context=context, status_code=status.HTTP_401_UNAUTHORIZED)