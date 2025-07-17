# main.py

from fastapi import FastAPI
from models import OperationRequest, OperationResult
from task_queue import background_worker
from controller import enqueue_math_operation
import logging.config
from logging_config import LOGGING_CONFIG

import asyncio

logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI()



@app.on_event("startup")
async def startup_event():
    # start the async background worker
    asyncio.create_task(background_worker())


@app.post("/compute", response_model=OperationResult)
async def compute(request: OperationRequest):
    return await enqueue_math_operation(request)
