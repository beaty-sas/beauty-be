from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import relationship

from beauty_be.models.base import Base
from beauty_be.models.base import BaseModel

business_offers = Table(
    'business_offers',
    Base.metadata,
    Column('business_id', Integer, ForeignKey('businesses.id')),
    Column('offer_id', Integer, ForeignKey('offers.id')),
)


class Business(BaseModel):
    __tablename__ = 'businesses'

    name = Column(String(200), unique=True, nullable=False, index=True)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    display_name = Column(String(200), nullable=False)
    phone_number = Column(String(100), nullable=True)
    description = Column(String(1000), nullable=True)

    owner_id = Column(Integer, ForeignKey('merchants.id'))
    logo_id = Column(Integer, ForeignKey('attachments.id'))
    banner_id = Column(Integer, ForeignKey('attachments.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))

    owner = relationship('Merchant', back_populates='businesses')
    logo = relationship('Attachment', back_populates='businesses_logo', foreign_keys=[logo_id])
    banner = relationship('Attachment', back_populates='businesses_banner', foreign_keys=[banner_id])
    location = relationship('Location', back_populates='businesses')
    working_hours = relationship('WorkingHours', back_populates='business')
    offers = relationship('Offer', secondary=business_offers, back_populates='businesses')
    bookings = relationship('Booking', back_populates='business')

    def __str__(self):
        return f'{self.id}: {self.name}'
