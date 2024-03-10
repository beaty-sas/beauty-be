from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from beauty_be.schemas.attachment import AttachmentSchema
from beauty_be.schemas.offer import OfferSchema
from beauty_be.schemas.user import UserSchema
from beauty_models.beauty_models.models import BookingStatus


class BookingSchema(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime
    offers: list[OfferSchema]
    user: UserSchema
    price: Decimal
    status: BookingStatus
    attachments: list[AttachmentSchema]
    comment: str

    class Config:
        from_attributes = True


class BookingCreateSchema(BaseModel):
    start_time: datetime
    business_id: int
    offers: list[int]
    user: UserSchema
    comment: str = ''
    attachments: list[int] = []


class BookingUpdateSchema(BaseModel):
    start_time: datetime
    end_time: datetime
    comment: str
