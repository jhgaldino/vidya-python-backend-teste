from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.db.mongo import get_text_collection
from app.db.sqlite import get_db
from app.schemas.sale import SaleCreate, SaleRead, SaleUpdate
from app.schemas.text import SaleTextCreate, SaleTextRead
from app.services import sales_service, text_service

router = APIRouter(prefix="/sales", tags=["sales"])


@router.post("", response_model=SaleRead, status_code=status.HTTP_201_CREATED)
def create_sale(payload: SaleCreate, db: Session = Depends(get_db)) -> SaleRead:
    sale = sales_service.create_sale(db, payload)
    if payload.text_note:
        collection = get_text_collection()
        text_service.create_text(collection, sale.id, payload.text_note)
    return sale


@router.get("", response_model=list[SaleRead])
def list_sales(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    category: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[SaleRead]:
    return sales_service.list_sales(db, start_date=start_date, end_date=end_date, category=category)


@router.get("/{sale_id}", response_model=SaleRead)
def get_sale(sale_id: int, db: Session = Depends(get_db)) -> SaleRead:
    sale = sales_service.get_sale(db, sale_id)
    if sale is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")
    return sale


@router.put("/{sale_id}", response_model=SaleRead)
def update_sale(sale_id: int, payload: SaleUpdate, db: Session = Depends(get_db)) -> SaleRead:
    sale = sales_service.get_sale(db, sale_id)
    if sale is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")
    return sales_service.update_sale(db, sale, payload)


@router.delete("/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale(sale_id: int, db: Session = Depends(get_db)) -> Response:
    sale = sales_service.get_sale(db, sale_id)
    if sale is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")

    sales_service.delete_sale(db, sale)
    text_service.delete_texts_by_sale_id(get_text_collection(), sale_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{sale_id}/texts", response_model=SaleTextRead, status_code=status.HTTP_201_CREATED)
def create_sale_text(
    sale_id: int,
    payload: SaleTextCreate,
    db: Session = Depends(get_db),
) -> SaleTextRead:
    sale = sales_service.get_sale(db, sale_id)
    if sale is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")

    doc = text_service.create_text(get_text_collection(), sale_id, payload.text)
    return SaleTextRead(id=doc["_id"], sale_id=doc["sale_id"], text=doc["text"])

