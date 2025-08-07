from fastapi import FastAPI
from Entities.models import OperationRequest, OperationResult
from Service.task_queue import background_worker
from Configurations_Settings.logging_config import LOGGING_CONFIG
from Repository.database import init_db
from Routes.math_operations_controller import router as operations_router
from fastapi.openapi.utils import get_openapi
import logging.config
import asyncio
from contextlib import asynccontextmanager


logging.config.dictConfig(LOGGING_CONFIG)


# lifespan handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # initialize DB tables
    asyncio.create_task(background_worker())  # start async worker
    yield


# FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)


# Including router
app.include_router(operations_router)


# Swagger UI global Bearer token authentication
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
