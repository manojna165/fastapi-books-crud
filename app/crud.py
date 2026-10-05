"""Data-access layer: all SQL lives here."""
import sqlite3
from typing import Optional

from .schemas import BookCreate, BookUpdate


def _row_to_dict(row: sqlite3.Row) -> dict:
    d = dict(row)
    d["in_stock"] = bool(d["in_stock"])
    return d


def list_books(db: sqlite3.Connection, skip: int = 0, limit: int = 100,
               author: Optional[str] = None) -> list[dict]:
    sql, params = "SELECT * FROM books", []
    if author:
        sql += " WHERE author LIKE ?"
        params.append(f"%{author}%")
    sql += " ORDER BY id LIMIT ? OFFSET ?"
    params += [limit, skip]
    return [_row_to_dict(r) for r in db.execute(sql, params).fetchall()]


def get_book(db: sqlite3.Connection, book_id: int) -> Optional[dict]:
    row = db.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    return _row_to_dict(row) if row else None


def get_book_by_isbn(db: sqlite3.Connection, isbn: str) -> Optional[dict]:
    row = db.execute("SELECT * FROM books WHERE isbn = ?", (isbn,)).fetchone()
    return _row_to_dict(row) if row else None


def create_book(db: sqlite3.Connection, book: BookCreate) -> dict:
    cur = db.execute(
        "INSERT INTO books (title, author, isbn, published_year, price, in_stock) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (book.title, book.author, book.isbn, book.published_year,
         book.price, int(book.in_stock)),
    )
    db.commit()
    return get_book(db, cur.lastrowid)


def update_book(db: sqlite3.Connection, book_id: int, book: BookUpdate) -> Optional[dict]:
    cur = db.execute(
        "UPDATE books SET title=?, author=?, isbn=?, published_year=?, price=?, in_stock=? "
        "WHERE id=?",
        (book.title, book.author, book.isbn, book.published_year,
         book.price, int(book.in_stock), book_id),
    )
    db.commit()
    return get_book(db, book_id) if cur.rowcount else None


def delete_book(db: sqlite3.Connection, book_id: int) -> bool:
    cur = db.execute("DELETE FROM books WHERE id = ?", (book_id,))
    db.commit()
    return cur.rowcount > 0
