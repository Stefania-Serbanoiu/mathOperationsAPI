# repository/database.py

from typing import Optional
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pydantic import BaseModel

# ---------- Database Configuration ----------

DATABASE_URL = "sqlite:///./operations.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

# ---------- SQLAlchemy ORM Model ----------

class DBOperationRecord(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    operation = Column(String, nullable=False)
    operand1 = Column(Integer, nullable=False)
    operand2 = Column(Integer, nullable=True)
    result = Column(Integer, nullable=False)

# ---------- Pydantic Schema for API ----------

class DBOperationRecordSchema(BaseModel):
    id: int
    timestamp: datetime
    operation: str
    operand1: int
    operand2: Optional[int]
    result: int

    model_config = {"from_attributes": True}

# ---------- DB Initialization ----------

def init_db():
    Base.metadata.create_all(bind=engine)
