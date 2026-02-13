from pydantic import BaseModel, Field

from app.schemas.sale import SaleRead


class SaleTextCreate(BaseModel):
    text: str = Field(min_length=1)


class SaleTextRead(BaseModel):
    id: str
    sale_id: int
    text: str


class TextSearchResult(BaseModel):
    text_id: str
    sale_id: int
    text: str
    sale: SaleRead

