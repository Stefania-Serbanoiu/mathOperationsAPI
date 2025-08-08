from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
import logging.config
import asyncio
from Service.task_queue import background_worker
from Configurations_Settings.logging_config import LOGGING_CONFIG
from Configurations_Settings.rabbitmq_log_handler import RabbitMQHandler
from Repository.database import init_db
from Routes.math_operations_controller import router as operations_router


# Configuration for logging (file + console from config)
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger()  # root logger


rabbit_handler = RabbitMQHandler(
    host='localhost',  # address of rabbitmq
    port=5672,
    queue='logs'
)
rabbit_handler.setLevel(logging.INFO)
rabbit_handler.setFormatter(logging.
                            Formatter("[%(asctime)s] %(levelname)s "
                                      "in %(name)s: %(message)s"))
logger.addHandler(rabbit_handler)


logger.info("Logging system initialized (file, console, and RabbitMQ).")


for handler in logging.getLogger().handlers:
    print(f"Attached handler: {handler.__class__.__name__}")


# FastAPI lifespan: initializing DB + start worker
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App startup: initializing DB and background worker...")
    init_db()
    asyncio.create_task(background_worker())
    logger.info("Background worker launched.")
    yield


# FastAPI app instance
app = FastAPI(lifespan=lifespan)


# Registering routes
app.include_router(operations_router)


# Swagger UI global Bearer token auth
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Async Math API",
        version="1.0.0",
        description="API for asynchronous math "
                    "operations with Bearer token protection",
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
