from datetime import datetime
from uuid import uuid4
from passlib.hash import argon2

from fastapi import Request
from sqlalchemy import select, delete

from app.schemas.user import UserSchema

from database.models.sessions import SessionModel
from database.models.users import UserModel

from utils.db import get_db

class SessionController:
    @staticmethod
    async def create(name: str, password: str, request: Request) -> str|None:
        token = uuid4().hex

        user_agent = request.headers.get("user-agent")
        created = datetime.now()
        
        async with await get_db() as db:
            user_result = await db.execute(select(UserModel).where(
                (UserModel.username == name)
            ))

            user = user_result.scalar()

            if not user:
                return None
            
            valid = argon2.verify(password, user.password)

            if not valid:
                return None

            session = SessionModel(
                token=token,
                user_id=user.id,
                created=created,
                user_agent=user_agent
            )
            
            db.add(session)
            await db.commit()
            await db.refresh(session)

        return token

    @staticmethod
    async def delete(token: str) -> bool:
        async with await get_db() as db:
            await db.execute(delete(SessionModel).where(
                (SessionModel.token == token)
            ))

            return True