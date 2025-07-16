# controller.py

from fastapi import HTTPException
from models import OperationRequest, OperationResult
from operations_service import perform_power, perform_fibonacci, perform_factorial
from exceptions import MissingOperandError, NegativeNumberError, UnsupportedOperationError


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

        return OperationResult(operation=op, input=request, result=result)

    except MissingOperandError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NegativeNumberError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UnsupportedOperationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
