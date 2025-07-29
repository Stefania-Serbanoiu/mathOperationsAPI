# task_queue.py

from Repository.database import SessionLocal, DBOperationRecord
from Repository.cache import generate_key, get_cached_result, set_cache

import asyncio
from Entities.models import OperationResult
from Service.operations_service import perform_power, perform_fibonacci, perform_factorial
from Entities.exceptions import (
    UnsupportedOperationError,
)
import logging

logger = logging.getLogger(__name__)

# async task queue
task_queue = asyncio.Queue()


async def background_worker():
    while True:
        request, future = await task_queue.get()
        op = request.mathematical_operation.lower()
        key = generate_key(op, request.mathematical_operand_1, request.mathematical_operand_2)

        try:
            cached_result = get_cached_result(key)
            if cached_result:
                logger.info(f"Cache HIT for key: {key}")
                future.set_result(cached_result)
                task_queue.task_done()
                continue

            # Compute
            if op == "pow":
                result = perform_power(request.mathematical_operand_1, request.mathematical_operand_2)
            elif op == "fib":
                result = perform_fibonacci(request.mathematical_operand_1)
            elif op == "fact":
                result = perform_factorial(request.mathematical_operand_1)
            else:
                raise UnsupportedOperationError(f"Unsupported operation: {op}")

            op_result = OperationResult(mathematical_operation_name=op, given_input_for_computing_operation=request, result=result)

            # Save to DB
            db = SessionLocal()
            db_record = DBOperationRecord(
                mathematical_operation_name=op,
                math_operand_1=request.mathematical_operand_1,
                math_operand_2=request.mathematical_operand_2,
                computation_result=result
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

