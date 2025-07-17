# controller.py

import asyncio
from fastapi import HTTPException
from models import OperationRequest, OperationResult
from task_queue import task_queue




async def enqueue_math_operation(request: OperationRequest) -> OperationResult:
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    await task_queue.put((request, future))

    try:
        result: OperationResult = await future
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
