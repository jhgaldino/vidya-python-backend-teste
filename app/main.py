import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pymongo.errors import PyMongoError
from sqlalchemy.exc import SQLAlchemyError

from app.api.routes.analytics import router as analytics_router
from app.api.routes.sales import router as sales_router
from app.api.routes.search import router as search_router
from app.core.config import get_settings
from app.db.mongo import create_indexes
from app.db.sqlite import create_tables

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0")
logger = logging.getLogger(__name__)


def initialize_data_stores() -> None:
    create_tables()
    create_indexes()


@app.on_event("startup")
def on_startup() -> None:
    initialize_data_stores()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    logger.warning("Validation error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "error_code": "validation_error",
            "errors": exc.errors(),
        },
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    logger.warning("Value error on %s %s: %s", request.method, request.url.path, exc)
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc),
            "error_code": "invalid_request",
        },
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    logger.exception("SQL error on %s %s", request.method, request.url.path, exc_info=exc)
    return JSONResponse(
        status_code=503,
        content={
            "detail": "Database temporarily unavailable",
            "error_code": "sql_database_error",
        },
    )


@app.exception_handler(PyMongoError)
async def pymongo_error_handler(request: Request, exc: PyMongoError) -> JSONResponse:
    logger.exception("Mongo error on %s %s", request.method, request.url.path, exc_info=exc)
    return JSONResponse(
        status_code=503,
        content={
            "detail": "Text database temporarily unavailable",
            "error_code": "mongo_database_error",
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error on %s %s", request.method, request.url.path, exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_code": "internal_server_error",
        },
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(sales_router)
app.include_router(analytics_router)
app.include_router(search_router)

initialize_data_stores()
