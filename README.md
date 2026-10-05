# Books CRUD API — FastAPI + Pydantic + SQLite

A REST API for managing a collection of books, with full Create / Read / Update / Delete support.

| Layer         | Technology                           |
|---------------|--------------------------------------|
| Web framework | FastAPI                              |
| Validation    | Pydantic                             |
| Database      | SQLite (Python's built-in `sqlite3`) |
| Server        | Uvicorn                              |

## Project structure

```
fastapi-books-crud/
├── app/
│   ├── __init__.py
│   ├── main.py        # FastAPI app and route handlers
│   ├── schemas.py     # Pydantic models (validation rules)
│   ├── crud.py        # SQL data-access functions
│   └── database.py    # SQLite connection + table creation
├── requirements.txt
├── README.md
└── Task1_FastAPI_CRUD_Report.pdf   # API testing report with screenshots
```

## Setup

Requires Python 3.9+.

```bash
python -m venv venv
venv\Scripts\activate          # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The server starts at <http://127.0.0.1:8000>. The SQLite file `books.db` and the
`books` table are created automatically on first start.

## Testing the API

Open Swagger UI at <http://127.0.0.1:8000/docs>, expand an endpoint,
click **Try it out → Execute**.

Test results with screenshots are in `Task1_FastAPI_CRUD_Report.pdf`.

## Data model

| Field            | Type   | Rules                         |
|------------------|--------|-------------------------------|
| `id`             | int    | Auto-generated                |
| `title`          | string | 1–200 chars, required         |
| `author`         | string | 1–120 chars, required         |
| `isbn`           | string | 10–17 chars, required, unique |
| `published_year` | int    | 1000–2100, required           |
| `price`          | float  | > 0, required                 |
| `in_stock`       | bool   | optional, default `true`      |

## API reference

| Method | Endpoint      | Description                            | Success | Errors        |
|--------|---------------|----------------------------------------|---------|---------------|
| GET    | `/`           | Health check                           | 200     | —             |
| POST   | `/books/`     | Create a book                          | 201     | 409, 422      |
| GET    | `/books/`     | List books (`skip`, `limit`, `author`) | 200     | 422           |
| GET    | `/books/{id}` | Get one book                           | 200     | 404           |
| PUT    | `/books/{id}` | Replace a book (all fields)            | 200     | 404, 409, 422 |
| DELETE | `/books/{id}` | Delete a book                          | 204     | 404           |

Error codes: **404** not found · **409** duplicate ISBN · **422** validation failure.

## Example request

```bash
curl -X POST http://127.0.0.1:8000/books/ -H "Content-Type: application/json" \
  -d '{"title":"Clean Code","author":"Robert C. Martin","isbn":"978-0132350884","published_year":2008,"price":33.99}'
```