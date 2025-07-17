# task_queue.py

import asyncio
from typing import Callable
from models import OperationRequest, OperationResult
from operations_service import perform_power, perform_fibonacci, perform_factorial
from exceptions import (
    MissingOperandError,
    NegativeNumberError,
    UnsupportedOperationError,
)
import logging

logger = logging.getLogger(__name__)

# async task queue
task_queue = asyncio.Queue()


async def background_worker():
    while True:
        request, future = await task_queue.get()
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

            op_result = OperationResult(operation=op, input=request, result=result)
            logger.info(f"SUCCESS: Operation '{op}' with input {request.dict()} resulted in {result}")
            future.set_result(op_result)

        except Exception as e:
            logger.exception(f"ERROR during '{op}' with input {request.dict()}: {e}")
            future.set_exception(e)

        task_queue.task_done()
