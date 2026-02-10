from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.sale import Sale
from app.schemas.sale import AnalyticsSummary, QuantityByCategory


def get_summary(
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None,
    category: str | None = None,
) -> AnalyticsSummary:
    revenue_expr = Sale.quantity * Sale.unit_price
    query = select(
        func.count(Sale.id).label("total_sales"),
        func.coalesce(func.sum(revenue_expr), 0).label("total_revenue"),
        func.coalesce(func.avg(revenue_expr), 0).label("average_ticket"),
    )

    if start_date:
        query = query.where(Sale.sale_date >= start_date)
    if end_date:
        query = query.where(Sale.sale_date <= end_date)
    if category:
        query = query.where(Sale.category == category)

    row = db.execute(query).one()
    return AnalyticsSummary(
        total_sales=int(row.total_sales),
        total_revenue=float(row.total_revenue),
        average_ticket=float(row.average_ticket),
    )


def get_quantity_by_category(
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[QuantityByCategory]:
    query = (
        select(
            Sale.category.label("category"),
            func.sum(Sale.quantity).label("total_quantity"),
        )
        .group_by(Sale.category)
        .order_by(func.sum(Sale.quantity).desc())
    )

    if start_date:
        query = query.where(Sale.sale_date >= start_date)
    if end_date:
        query = query.where(Sale.sale_date <= end_date)

    rows = db.execute(query).all()
    return [
        QuantityByCategory(category=row.category, total_quantity=int(row.total_quantity))
        for row in rows
    ]

