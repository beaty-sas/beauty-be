from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from beauty_be.schemas.business import BaseBusinessSchema
from beauty_be.schemas.user import UserSchema


class BookingSchema(BaseModel):
    start_time: datetime
    end_time: datetime
    business: BaseBusinessSchema
    price: Decimal

    class Config:
        from_attributes = True


class BookingCreateSchema(BaseModel):
    start_time: datetime
    business_id: int
    offers: list[int]
    user: UserSchema
