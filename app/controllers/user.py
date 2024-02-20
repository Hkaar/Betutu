from passlib.hash import argon2

from sqlalchemy import select, delete

from database.models.users import UserModel

from utils.db import get_db

class UserController:
    @staticmethod
    async def create(name: str, password: str) -> bool:
        async with await get_db() as db:
            exist = await db.execute(select(UserModel).where(
                UserModel.username == name
            ))

            if exist.scalar():
                return False
            
            hashed = argon2.using(rounds=4).hash(password)
            
            user = UserModel(
                username=name,
                password=hashed
            )

            db.add(user)
            await db.commit()
            await db.refresh(user)
        return True

    @staticmethod
    async def get(name: str, password: str) -> bool:
        async with await get_db() as db:
            stored_password = await db.execute(select(UserModel.password).where(
                (UserModel.username == name)
            ))

            hashed = stored_password.scalar()

            valid = argon2.verify(password, hashed)

            if valid:
                return True
        return False

    @staticmethod
    async def delete(name: str, password: str) -> bool:
        async with await get_db() as db:
            stored_password = await db.execute(select(UserModel.password).where(
                (UserModel.username == name)
            ))

            valid = argon2.verify(password, stored_password.scalar())

            if valid and name != "root":
                await db.execute(delete(UserModel).where(
                    (UserModel.username == name)
                ))
                return True
        return False
