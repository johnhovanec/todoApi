from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Pydantic models

# Base class
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