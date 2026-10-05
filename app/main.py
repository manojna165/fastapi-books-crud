"""FastAPI application: CRUD endpoints for a Books resource."""
import sqlite3
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status

from . import crud
from .database import get_db, init_db
from .schemas import BookCreate, BookOut, BookUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # create tables on startup
    yield


app = FastAPI(
    title="Books CRUD API",
    description="A simple CRUD REST API built with FastAPI, Pydantic and SQLite.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Books CRUD API is running", "docs": "/docs"}


@app.post("/books/", response_model=BookOut, status_code=status.HTTP_201_CREATED,
          tags=["Books"], summary="Create a book")
def create_book(book: BookCreate, db: sqlite3.Connection = Depends(get_db)):
    if crud.get_book_by_isbn(db, book.isbn):
        raise HTTPException(status.HTTP_409_CONFLICT,
                            f"A book with ISBN {book.isbn} already exists")
    return crud.create_book(db, book)


@app.get("/books/", response_model=list[BookOut], tags=["Books"],
         summary="List books (pagination + author filter)")
def list_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    author: Optional[str] = Query(None, description="Case-insensitive partial match"),
    db: sqlite3.Connection = Depends(get_db),
):
    return crud.list_books(db, skip, limit, author)


@app.get("/books/{book_id}", response_model=BookOut, tags=["Books"],
         summary="Get a book by ID")
def read_book(book_id: int, db: sqlite3.Connection = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Book not found")
    return book


@app.put("/books/{book_id}", response_model=BookOut, tags=["Books"],
         summary="Update (replace) a book")
def update_book(book_id: int, book: BookUpdate, db: sqlite3.Connection = Depends(get_db)):
    if crud.get_book(db, book_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Book not found")
    existing = crud.get_book_by_isbn(db, book.isbn)
    if existing and existing["id"] != book_id:
        raise HTTPException(status.HTTP_409_CONFLICT,
                            f"A book with ISBN {book.isbn} already exists")
    return crud.update_book(db, book_id, book)


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT,
            tags=["Books"], summary="Delete a book")
def delete_book(book_id: int, db: sqlite3.Connection = Depends(get_db)):
    if not crud.delete_book(db, book_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Book not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
