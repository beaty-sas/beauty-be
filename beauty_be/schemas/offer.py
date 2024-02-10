from decimal import Decimal

from pydantic import BaseModel


class OfferSchema(BaseModel):
    name: str
    price: Decimal
    duration: int

    class Config:
        from_attributes = True
