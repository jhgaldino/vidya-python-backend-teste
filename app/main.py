from fastapi import FastAPI

from app.api.routes.analytics import router as analytics_router
from app.api.routes.sales import router as sales_router
from app.api.routes.search import router as search_router
from app.core.config import get_settings
from app.db.mongo import create_indexes
from app.db.sqlite import create_tables

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0")


def initialize_data_stores() -> None:
    create_tables()
    create_indexes()


@app.on_event("startup")
def on_startup() -> None:
    initialize_data_stores()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(sales_router)
app.include_router(analytics_router)
app.include_router(search_router)

initialize_data_stores()
