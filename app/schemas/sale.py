from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SaleBase(BaseModel):
    product_name: str = Field(min_length=1, max_length=255)
    category: str = Field(min_length=1, max_length=100)
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(gt=0, decimal_places=2, max_digits=12)
    sale_date: date


class SaleCreate(SaleBase):
    text_note: str | None = Field(default=None, min_length=1)


class SaleUpdate(BaseModel):
    product_name: str | None = Field(default=None, min_length=1, max_length=255)
    category: str | None = Field(default=None, min_length=1, max_length=100)
    quantity: int | None = Field(default=None, gt=0)
    unit_price: Decimal | None = Field(default=None, gt=0, decimal_places=2, max_digits=12)
    sale_date: date | None = None


class SaleRead(SaleBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AnalyticsSummary(BaseModel):
    total_sales: int
    total_revenue: Decimal
    average_ticket: Decimal


class QuantityByCategory(BaseModel):
    category: str
    total_quantity: int

