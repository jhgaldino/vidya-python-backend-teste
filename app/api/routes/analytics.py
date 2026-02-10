from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.sqlite import get_db
from app.schemas.sale import AnalyticsSummary, QuantityByCategory
from app.services import analytics_service

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary", response_model=AnalyticsSummary)
def get_summary(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    category: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> AnalyticsSummary:
    return analytics_service.get_summary(
        db,
        start_date=start_date,
        end_date=end_date,
        category=category,
    )


@router.get("/quantity-by-category", response_model=list[QuantityByCategory])
def get_quantity_by_category(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[QuantityByCategory]:
    return analytics_service.get_quantity_by_category(
        db,
        start_date=start_date,
        end_date=end_date,
    )

