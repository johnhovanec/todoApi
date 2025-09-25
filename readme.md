# FastAPI To-Do API

FastAPI app that connects to MS SQL Server using SQLAlchemy + pyodbc.

Setup
1. Create a virtual environment and activate it.

```bash
python -m venv .venv
source .venv/Scripts/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Ensure you have an appropriate ODBC driver installed on Windows, e.g. "ODBC Driver 17 for SQL Server" or newer. Download from Microsoft if needed.

4. Put your connection URL in `.env` as `DATABASE_URL`. Example format when using a full SQLAlchemy URL:

```
DATABASE_URL="mssql+pyodbc://user:pass@(localdb)\\MSSQLLocalDB/DatabaseName?driver=ODBC+Driver+17+for+SQL+Server"
```

Running

```bash
uvicorn main:app --reload
```

## Endpoints
The endpoints query a single table: dbo.Task  

- `GET /` - "Hello Todo API"
- `GET /tasks/` - Returns all tasks 
- `GET /tasks/{id}` - Returns a single task by id
- `POST /tasks/` - Add a task to the database
- `PATCH /tasks/{id}` - Marks a specific task by id as completed
- `DELETE /tasks/{id}` - Deletes the specific task by id

## Project Structure
- `schema.py` holds Pydantic models
- `models.py` holds SQLAlchemy models
