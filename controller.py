# controller.py

import logging
from fastapi import HTTPException
from models import OperationRequest, OperationResult
from operations_service import perform_power, perform_fibonacci, perform_factorial
from exceptions import MissingOperandError, NegativeNumberError, UnsupportedOperationError

logger = logging.getLogger(__name__)


def compute_operation(request: OperationRequest) -> OperationResult:
    op = request.operation.lower()

    try:
        if op == "pow":
            result = perform_power(request.operand1, request.operand2)
        elif op == "fib":
            result = perform_fibonacci(request.operand1)
        elif op == "fact":
            result = perform_factorial(request.operand1)
        else:
            raise UnsupportedOperationError(f"Unsupported operation: {op}")

        logger.info(f"SUCCESS: Operation '{op}' with input {request.dict()} resulted in {result}")
        return OperationResult(operation=op, input=request, result=result)

    except (MissingOperandError, NegativeNumberError, UnsupportedOperationError) as e:
        logger.error(f"CLIENT ERROR: Operation '{op}' with input {request.dict()} failed due to: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"SERVER ERROR: Unexpected error during operation '{op}' with input {request.dict()}")
        raise HTTPException(status_code=500, detail="Internal server error")
