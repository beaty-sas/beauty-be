from decimal import Decimal

from pydantic import BaseModel


class OfferSchema(BaseModel):
    id: int
    name: str
    price: Decimal
    duration: int

    class Config:
        from_attributes = True


class CreateOfferRequestSchema(BaseModel):
    name: str
    price: Decimal
    duration: int
    business_id: int
