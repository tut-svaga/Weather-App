# backend/app/models/quote.py

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Quote(Base):
    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str | None] = mapped_column(String(255), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)

    def __repr__(self) -> str:
        return f"<Quote id={self.id} author={self.author!r}>"
