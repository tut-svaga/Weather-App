# backend/app/database.py

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://quotes_user:password@postgres:5432/quotes_db",
)

# Render provides PostgreSQL URLs with the sync ``postgresql://`` scheme.
# This application uses SQLAlchemy's async engine, so select asyncpg explicitly.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

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
