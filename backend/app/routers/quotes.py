# backend/app/routers/quotes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.quote import Quote
from app.schemas.quote import QuoteCreate, QuoteResponse

router = APIRouter(prefix="/quotes", tags=["quotes"])


# ── GET /api/quotes/random ────────────────────────────────────────────────────
@router.get("/random", response_model=QuoteResponse)
async def get_random_quote(db: AsyncSession = Depends(get_db)):
    """Возвращает случайную цитату при каждом запросе."""
    result = await db.execute(
        select(Quote).order_by(func.random()).limit(1)
    )
    quote = result.scalar_one_or_none()
    if not quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Цитаты не найдены. Сначала запусти seed.py.",
        )
    return quote


# ── GET /api/quotes/ ──────────────────────────────────────────────────────────
@router.get("/", response_model=list[QuoteResponse])
async def get_all_quotes(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """Все цитаты с пагинацией."""
    result = await db.execute(select(Quote).offset(skip).limit(limit))
    return result.scalars().all()


# ── GET /api/quotes/{id} ──────────────────────────────────────────────────────
@router.get("/{quote_id}", response_model=QuoteResponse)
async def get_quote(quote_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Quote).where(Quote.id == quote_id))
    quote = result.scalar_one_or_none()
    if not quote:
        raise HTTPException(status_code=404, detail="Цитата не найдена")
    return quote


# ── POST /api/quotes/ (опционально — для добавления через API) ────────────────
@router.post("/", response_model=QuoteResponse, status_code=status.HTTP_201_CREATED)
async def create_quote(payload: QuoteCreate, db: AsyncSession = Depends(get_db)):
    quote = Quote(**payload.model_dump())
    db.add(quote)
    await db.commit()
    await db.refresh(quote)
    return quote
