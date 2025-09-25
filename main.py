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

########## Pydantic models ###########
class TaskBase(BaseModel):
    id: int
    description: Optional[str] = None
    createdate: Optional[str] = None
    completiondate: Optional[str] = None

# for reading response
class TaskOut(BaseModel):
    id: int
    description: Optional[str] = None
    createdate: Optional[datetime] = None
    completiondate: Optional[datetime] = None

    class Config:
        from_attributes = True

# for partial updates using PATCH
class TaskUpdate(BaseModel):
    description: Optional[str] = None
    completiondate: Optional[datetime] = None

# For creating a new task using POST
class TaskCreate(BaseModel):
    description: str
    createdate: Optional[datetime] = None


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

# PATCH update task by id
@app.patch("/tasks/{id}", response_model=TaskOut)
def update_task(id: int, db: Session = Depends(get_db)):
    # Get the task from DB by id to update
    db_task = db.query(models.Task).filter(models.Task.id == id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Set completiondate to now
    db_task.completiondate = datetime.now()

    db.commit()
    db.refresh(db_task)
    return db_task

# POST create a new task
@app.post("/tasks/", response_model=TaskOut)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(
        description = task.description,
        createdate = datetime.now(),
        completiondate =None
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# DELETE task by id
@app.delete("/tasks/{id}")
def delete_task(id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted for id {}".format(id)}