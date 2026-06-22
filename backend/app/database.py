# backend/app/database.py

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://quotes_user:password@postgres:5432/quotes_db",
)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,          # поставь True если нужно видеть SQL в логах
    pool_size=10,
    max_overflow=20,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db():
    """Dependency для FastAPI — инжектит сессию в роутеры."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
