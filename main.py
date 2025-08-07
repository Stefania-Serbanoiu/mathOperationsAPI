from fastapi import FastAPI
from Entities.models import OperationRequest, OperationResult
from Service.task_queue import background_worker
from Routes.math_operations_async_mechanism import enqueue_math_operation
import logging.config
from Configurations_Settings.logging_config import LOGGING_CONFIG
from Repository.database import init_db
import asyncio
from Routes.math_operations_controller import router as operations_router
from fastapi.openapi.utils import get_openapi


logging.config.dictConfig(LOGGING_CONFIG)


app = FastAPI()


app.include_router(operations_router)  # Register the router


@app.on_event("startup")
async def startup_event():
    init_db()  # initialize tables
    asyncio.create_task(background_worker())


@app.post("/compute", response_model=OperationResult)
async def compute(request: OperationRequest):
    return await enqueue_math_operation(request)


# Swagger UI Global Bearer Auth
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Async Math API",
        version="1.0.0",
        description="API for asynchronous math operations with Bearer token protection",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
