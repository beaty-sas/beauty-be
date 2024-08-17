from decimal import Decimal

from pydantic import BaseModel
from pydantic import ConfigDict


class OfferSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: Decimal
    duration: int
    allow_photo: bool


class CreateOfferRequestSchema(BaseModel):
    name: str
    price: Decimal
    duration: int
    business_id: int
    allow_photo: bool
