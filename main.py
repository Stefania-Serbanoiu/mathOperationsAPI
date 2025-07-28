# main.py

from fastapi import FastAPI
from Entities.models import OperationRequest, OperationResult
from Service.task_queue import background_worker
from CORS.math_operations_async_mechanism import enqueue_math_operation
import logging.config
from Configurations_Settings.logging_config import LOGGING_CONFIG
from Repository.database import init_db
import asyncio
from CORS.math_operations_controller import router as operations_router  # Import your router


logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI()

app.include_router(operations_router)  # Register the router

@app.on_event("startup")
async def startup_event():
    init_db()  # ← initialize tables

    # start the async background worker
    asyncio.create_task(background_worker())


@app.post("/compute", response_model=OperationResult)
async def compute(request: OperationRequest):
    return await enqueue_math_operation(request)
