from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic import BaseModel
from Configurations_Settings.app_settings import settings


# Database Configuration from .env
DATABASE_URL = settings.database_url  # loaded via Pydantic settings class


engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


Base = declarative_base()


class DBOperationRecord(Base):
    """
    SQLAlchemy ORM Model using SQAlchemy class 'Base'
    record -> db record representing data for a mathematical operation
    """
    __tablename__ = "operations"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    mathematical_operation_name = Column(String, nullable=False)
    math_operand_1 = Column(Integer, nullable=False)
    math_operand_2 = Column(Integer, nullable=True)
    computation_result = Column(Integer, nullable=False)


class DBOperationRecordSchema(BaseModel):
    """
    Pydantic Schema for API , inheriting from pydantic 'BaseModel' class
    """
    id: int
    timestamp: datetime
    mathematical_operation_name: str
    math_operand_1: int
    math_operand_2: Optional[int]
    computation_result: int

    model_config = {"from_attributes": True}


def init_db():
    """
    DB Initialization (SQLite database initialization using sqlalchemy)
    """
    Base.metadata.create_all(bind=engine)
