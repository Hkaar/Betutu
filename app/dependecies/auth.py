from datetime import datetime, timedelta

from fastapi import Request, HTTPException, status

from sqlalchemy import select, delete
from database.models.sessions import SessionModel

from utils.db import get_db

class SessionAuth:
    async def clear_sessions():
        current = datetime.utcnow()
        expire = current - timedelta(days=1)
        
        async with await get_db() as db:
            await db.execute(delete(SessionModel).where(
                SessionModel.created <= expire
            ))

            await db.commit()

    async def validate_session(request: Request):
        await SessionAuth.clear_sessions()

        token = request.cookies.get("sessionToken", "")

        async with await get_db() as db:
            exist = await db.execute(select(SessionModel).where(
                (SessionModel.token == token)
            ))

            if exist.scalar():
                return True
        
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            detail="Opps looks like you're not authorized! Please try again!",
            headers={"Location": "/error/401"}
        )