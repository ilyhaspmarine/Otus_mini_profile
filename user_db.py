from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os
from urllib.parse import urlunparse

driver = os.getenv("DB_DRIVER_ASYNC", "asyncpg")
if not driver:
    raise ValueError("The USERS_DB_DRIVER_SYNC environment variable is not set.")
driver = "postgresql+" + driver
username = os.getenv("DB_USER", "username")
password = os.getenv("DB_PASSWORD", "username")
host = os.getenv("DB_HOST", "postgre")
port = os.getenv("DB_PORT", "5432")
database = os.getenv("DB_NAME", "users")

comp = (
    driver,  # scheme
    f"{username}:{password}@{host}:{port}",  # netloc
    database,  # path
    "",  # params
    "",  # query
    "",  # fragment
)

url = urlunparse(comp)

engine = create_async_engine(url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session