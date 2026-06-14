#!/usr/bin/env python3
# backend/seed.py
# Запуск: python seed.py
# (из директории backend, при запущенной БД)

import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.models.quote import Quote
from app.database import Base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://quotes_user:password@localhost:5432/quotes_db",
)

QUOTES = [
    {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs", "category": "motivation"},
    {"text": "In the middle of every difficulty lies opportunity.", "author": "Albert Einstein", "category": "inspiration"},
    {"text": "Life is what happens when you're busy making other plans.", "author": "John Lennon", "category": "life"},
    {"text": "Get busy living or get busy dying.", "author": "Stephen King", "category": "motivation"},
    {"text": "You only live once, but if you do it right, once is enough.", "author": "Mae West", "category": "life"},
    {"text": "In three words I can sum up everything I've learned about life: it goes on.", "author": "Robert Frost", "category": "life"},
    {"text": "To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment.", "author": "Ralph Waldo Emerson", "category": "inspiration"},
    {"text": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius", "category": "motivation"},
    {"text": "Everything you've ever wanted is on the other side of fear.", "author": "George Addair", "category": "motivation"},
    {"text": "Success is not final, failure is not fatal: it is the courage to continue that counts.", "author": "Winston Churchill", "category": "success"},
    {"text": "Hardships often prepare ordinary people for an extraordinary destiny.", "author": "C.S. Lewis", "category": "inspiration"},
    {"text": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt", "category": "motivation"},
    {"text": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt", "category": "motivation"},
    {"text": "It is during our darkest moments that we must focus to see the light.", "author": "Aristotle", "category": "inspiration"},
    {"text": "Do not go where the path may lead, go instead where there is no path and leave a trail.", "author": "Ralph Waldo Emerson", "category": "inspiration"},
    {"text": "You will face many defeats in life, but never let yourself be defeated.", "author": "Maya Angelou", "category": "motivation"},
    {"text": "The greatest glory in living lies not in never falling, but in rising every time we fall.", "author": "Nelson Mandela", "category": "inspiration"},
    {"text": "In the end, it's not the years in your life that count. It's the life in your years.", "author": "Abraham Lincoln", "category": "life"},
    {"text": "Never let the fear of striking out keep you from playing the game.", "author": "Babe Ruth", "category": "motivation"},
    {"text": "Life is either a daring adventure or nothing at all.", "author": "Helen Keller", "category": "life"},
    {"text": "Many of life's failures are people who did not realize how close they were to success when they gave up.", "author": "Thomas A. Edison", "category": "success"},
    {"text": "The only impossible journey is the one you never begin.", "author": "Tony Robbins", "category": "motivation"},
    {"text": "Do not dwell in the past, do not dream of the future, concentrate the mind on the present moment.", "author": "Buddha", "category": "mindfulness"},
    {"text": "The secret of getting ahead is getting started.", "author": "Mark Twain", "category": "motivation"},
    {"text": "It always seems impossible until it's done.", "author": "Nelson Mandela", "category": "motivation"},
    {"text": "Don't watch the clock; do what it does. Keep going.", "author": "Sam Levenson", "category": "motivation"},
    {"text": "Keep your face always toward the sunshine, and shadows will fall behind you.", "author": "Walt Whitman", "category": "inspiration"},
    {"text": "Whether you think you can or you think you can't, you're right.", "author": "Henry Ford", "category": "motivation"},
    {"text": "The best time to plant a tree was 20 years ago. The second best time is now.", "author": "Chinese Proverb", "category": "wisdom"},
    {"text": "An unexamined life is not worth living.", "author": "Socrates", "category": "wisdom"},
]


async def seed():
    engine = create_async_engine(DATABASE_URL, echo=True)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_factory() as session:
        # Проверяем, есть ли уже данные
        from sqlalchemy import select, func
        count_result = await session.execute(select(func.count()).select_from(Quote))
        count = count_result.scalar()
        if count > 0:
            print(f"БД уже содержит {count} цитат. Seed пропущен.")
            return

        quotes = [Quote(**q) for q in QUOTES]
        session.add_all(quotes)
        await session.commit()
        print(f"✅ Добавлено {len(quotes)} цитат в БД.")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
