#models.py

from pydantic import BaseModel, Field
from datetime import datetime

"""Entity domain classes are defined by inheriting from pydantic BaseModel class"""

class OperationRequest(BaseModel):
    """
    Represents an input to the system (input defining a mathematical operation supported by the system)
    """
    mathematical_operation: str = Field(..., description="One of: pow(power computation), fib(the n-th fibonacci number), fact(the factorial of a number)")
    mathematical_operand_1: int = Field(..., description="First number (required)")
    mathematical_operand_2: int | None = Field(None, description="Second number (used only for pow - for exponent operand)")


class OperationResult(BaseModel):
    """
    Represents the result of a mathematical computation, along with the original input
    """
    mathematical_operation_name: str
    given_input_for_computing_operation: OperationRequest
    result: int

"""
class DBRecord(BaseModel):
    id: Optional[int] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    operation: str
    operand1: int
    operand2: Optional[int] = None
    result: int

    model_config = {
        "from_attributes": True
    }
"""


class CachedOperation(BaseModel):
    """
    Represents a cache entry for previously computed results
    Useful for in-memory caching using dict
    """
    key: str  # Can be generated like f"{operation}:{operand1}:{operand2 or ''}"
    value: OperationResult
    cached_at_datetime: datetime = Field(default_factory=datetime.utcnow)
