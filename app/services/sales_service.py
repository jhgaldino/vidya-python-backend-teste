from datetime import date

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.sale import Sale
from app.schemas.sale import SaleCreate, SaleUpdate


def create_sale(db: Session, payload: SaleCreate) -> Sale:
    sale = Sale(
        product_name=payload.product_name,
        category=payload.category,
        quantity=payload.quantity,
        unit_price=payload.unit_price,
        sale_date=payload.sale_date,
    )
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale


def get_sale(db: Session, sale_id: int) -> Sale | None:
    return db.get(Sale, sale_id)


def list_sales(
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None,
    category: str | None = None,
) -> list[Sale]:
    query: Select[tuple[Sale]] = select(Sale)

    if start_date:
        query = query.where(Sale.sale_date >= start_date)
    if end_date:
        query = query.where(Sale.sale_date <= end_date)
    if category:
        query = query.where(Sale.category == category)

    query = query.order_by(Sale.sale_date.desc(), Sale.id.desc())
    return list(db.scalars(query).all())


def update_sale(db: Session, sale: Sale, payload: SaleUpdate) -> Sale:
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(sale, key, value)

    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale


def delete_sale(db: Session, sale: Sale) -> None:
    db.delete(sale)
    db.commit()

