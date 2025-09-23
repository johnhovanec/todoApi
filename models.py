from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Task(Base):
    __tablename__ = "Task"  # table name in MSSQL

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(1000))
    createdate = Column(DateTime)
    completiondate = Column(DateTime)
