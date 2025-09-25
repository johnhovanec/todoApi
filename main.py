from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from pydantic import BaseModel
from typing import Optional
import models

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with MSSQL"}

# GET all tasks
@app.get("/tasks/")
def read_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks

# GET task by id
@app.get("/tasks/{id}")
def read_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task detail not found")
    return task

class TaskBase(BaseModel):
    id: int
    description: Optional[str] = None
    createdate: Optional[str] = None
    completiondate: Optional[str] = None

# for reading (response)
class TaskOut(BaseModel):
    id: int
    description: Optional[str] = None
    createdate: Optional[datetime] = None
    completiondate: Optional[datetime] = None

    class Config:
        from_attributes = True

# for partial updates (PATCH)
class TaskUpdate(BaseModel):
    description: Optional[str] = None
    completiondate: Optional[datetime] = None


@app.patch("/tasks/{id}", response_model=TaskOut)
def update_task(id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    # Get the task from DB by id to update
    db_task = db.query(models.Task).filter(models.Task.id == id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update only fields provided
    update_data = task_update.model_dump(exclude_unset=True) 

    # Set the completiondate to now
    if "completiondate" not in update_data:
        update_data["completiondate"] = datetime.now()

    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task