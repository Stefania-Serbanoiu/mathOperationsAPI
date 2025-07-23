# task_queue.py

from repository.database import SessionLocal, DBOperationRecord
from repository.cache import generate_key, get_cached_result, set_cache

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
        key = generate_key(op, request.operand1, request.operand2)

        try:
            cached_result = get_cached_result(key)
            if cached_result:
                logger.info(f"Cache HIT for key: {key}")
                future.set_result(cached_result)
                task_queue.task_done()
                continue

            # Compute
            if op == "pow":
                result = perform_power(request.operand1, request.operand2)
            elif op == "fib":
                result = perform_fibonacci(request.operand1)
            elif op == "fact":
                result = perform_factorial(request.operand1)
            else:
                raise UnsupportedOperationError(f"Unsupported operation: {op}")

            op_result = OperationResult(operation=op, input=request, result=result)

            # Save to DB
            db = SessionLocal()
            db_record = DBOperationRecord(
                operation=op,
                operand1=request.operand1,
                operand2=request.operand2,
                result=result
            )
            db.add(db_record)
            db.commit()
            db.close()

            # Cache it
            set_cache(key, op_result)

            logger.info(f"SUCCESS: Computed {key} = {result}")
            future.set_result(op_result)

        except Exception as e:
            logger.exception(f"ERROR during '{op}' with input {request.dict()}: {e}")
            future.set_exception(e)

        task_queue.task_done()

