# backend/app/schemas/quote.py

from pydantic import BaseModel


class QuoteResponse(BaseModel):
    id: int
    text: str
    author: str | None = None
    category: str | None = None

    model_config = {"from_attributes": True}


class QuoteCreate(BaseModel):
    text: str
    author: str | None = None
    category: str | None = None
