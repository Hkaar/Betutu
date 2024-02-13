from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from utils.config import Settings

Settings.load_env()

engine = create_async_engine(Settings.get_env("DATABASE_URL"))
Base = declarative_base()

class DBManager:
    def __init__(self, engine):
        self.engine = engine

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def init(self):
        await self.create_tables()

    async def shutdown(self):
        await self.engine.dispose()

async def get_db():
    async with AsyncSession(engine) as session:
        yield session