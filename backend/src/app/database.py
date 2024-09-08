from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase



DATABASE_URL = ''

class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL)


async def get_async_session()-> AsyncGenerator[AsyncSession, None]:
    async with async_sessionmaker() as session:
        yield session

