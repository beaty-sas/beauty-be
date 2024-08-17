from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import DECIMAL
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import text
from sqlalchemy.orm import relationship

from beauty_be.models.base import BaseModel


class Offer(BaseModel):
    __tablename__ = 'offers'

    name = Column(String(200), unique=True, nullable=False)
    price = Column(DECIMAL(precision=10, scale=2), nullable=False)  # type: ignore
    duration = Column(Integer, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    allow_photo = Column(Boolean, nullable=True, server_default=text('false'))

    businesses = relationship('Business', secondary='business_offers', back_populates='offers')
    booking = relationship('Booking', secondary='booking_offers_association', back_populates='offers')

    def __str__(self):
        return f'{self.id}: {self.name}'
