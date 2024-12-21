import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

HOST = os.getenv("DATABASE_HOST", "localhost")
PORT = os.getenv("DATABASE_PORT", "7432")
USER = os.getenv("DATABASE_USER", "postgres")
PASSWORD = os.getenv("DATABASE_PASSWORD", "boot")
DATABASE = os.getenv("DATABASE_NAME", "muscule_sql")
print(f"HOST: {HOST}")
print(f"USER: {USER}")
print(f"PASSWORD: {PASSWORD}")
URL = f'postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
engine = create_async_engine(URL, echo=True)

AsyncSessionMaker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
