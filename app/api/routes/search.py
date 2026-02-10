from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.mongo import get_text_collection
from app.db.sqlite import get_db
from app.schemas.text import TextSearchResult
from app.services import sales_service, text_service

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/text", response_model=list[TextSearchResult])
def search_text(
    q: str = Query(min_length=1),
    db: Session = Depends(get_db),
) -> list[TextSearchResult]:
    docs = text_service.search_texts(get_text_collection(), q)
    results: list[TextSearchResult] = []

    for doc in docs:
        sale = sales_service.get_sale(db, int(doc["sale_id"]))
        if sale is None:
            continue
        results.append(
            TextSearchResult(
                text_id=doc["_id"],
                sale_id=int(doc["sale_id"]),
                text=doc["text"],
                sale=sale,
            )
        )

    return results

