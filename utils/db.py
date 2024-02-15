from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from utils.config import Settings

# Get database connection details from environment variables
CONNECTION = Settings.get_env("DB_CONNECTION")
CONNECTOR = Settings.get_env("DB_CONNECTOR")
HOST = Settings.get_env("DB_HOST")
PORT = Settings.get_env("DB_PORT")

USERNAME = Settings.get_env("DB_USERNAME")
DATABASE = Settings.get_env("DB_DATABASE")
PASSWORD = Settings.get_env("DB_PASSWORD")

# Construct the database URL based on the connection type
if CONNECTION == "sqlite":
    db_url = f"{CONNECTION}+{CONNECTOR}:///{DATABASE}"
else:
    db_url = f"{CONNECTION}+{CONNECTOR}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

# Create a base class for declarative models
Base = declarative_base()

class DBManager:
    engine: AsyncEngine | None = None

    @classmethod
    async def create_tables(cls):
        async with cls.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @classmethod
    async def init(cls):
        cls.engine = create_async_engine(db_url)
        
        await cls.create_tables()

    @classmethod
    async def shutdown(cls):
        await cls.engine.dispose()

async def get_db():
    async with AsyncSession(DBManager.engine) as session:
        return session