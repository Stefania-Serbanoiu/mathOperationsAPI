#models.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class OperationRequest(BaseModel):
    """
    Represents an input to the system
    """
    operation: str = Field(..., description="One of: pow, fib, fact")
    operand1: int = Field(..., description="First number (required)")
    operand2: Optional[int] = Field(None, description="Second number (used only for pow)")


class OperationResult(BaseModel):
    """
    Represents the result of a computation, along with the original input
    """
    operation: str
    input: OperationRequest
    result: int


class DBRecord(BaseModel):
    """
    A record of a stored/computed operation, with timestamp and optional ID
    Useful for SQLite/file-based logging
    """
    id: Optional[int] = None  # Auto-incremented in DB
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    operation: str
    operand1: int
    operand2: Optional[int] = None
    result: int


class CachedOperation(BaseModel):
    """
    Represents a cache entry for previously computed results
    Useful for in-memory caching using dict
    """
    key: str  # Can be generated like f"{operation}:{operand1}:{operand2 or ''}"
    value: OperationResult
    cached_at: datetime = Field(default_factory=datetime.utcnow)
