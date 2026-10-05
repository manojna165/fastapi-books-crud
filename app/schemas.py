"""Pydantic models: request validation and response serialization."""
from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, examples=["Clean Code"])
    author: str = Field(..., min_length=1, max_length=120, examples=["Robert C. Martin"])
    isbn: str = Field(..., min_length=10, max_length=17, examples=["978-0132350884"])
    published_year: int = Field(..., ge=1000, le=2100, examples=[2008])
    price: float = Field(..., gt=0, examples=[33.99])
    in_stock: bool = True


class BookCreate(BookBase):
    """Body for POST /books/."""


class BookUpdate(BookBase):
    """Body for PUT /books/{id} (full replacement)."""


class BookOut(BookBase):
    """Returned to clients; includes the DB-generated id."""
    model_config = ConfigDict(from_attributes=True)
    id: int
