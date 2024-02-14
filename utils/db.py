from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
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

# Create an async engine
engine = create_async_engine(db_url)

# Create a base class for declarative models
Base = declarative_base()

class DBManager:
    def __init__(self, engine):
        self.engine = engine

    async def create_tables(self):
        # Create tables based on declarative models
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def init(self):
        # Initialize the database, create tables, etc.
        await self.create_tables()

    async def shutdown(self):
        # Provide an async session for database operations
        await self.engine.dispose()

async def get_db():
    # Provide an async session for database operations
    async with AsyncSession(engine) as session:
        yield session