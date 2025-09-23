from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with MSSQL"}

@app.get("/tasks/")
def read_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks
