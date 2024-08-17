from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from beauty_be.models.base import BaseModel


class Merchant(BaseModel):
    __tablename__ = 'merchants'

    sub = Column(String(200), unique=True, nullable=False, index=True)
    display_name = Column(String(100), nullable=False)
    phone_number = Column(String(100), nullable=True)
    telegram_id = Column(String(100), nullable=True)

    logo_id = Column(Integer, ForeignKey('attachments.id'))

    logo = relationship('Attachment', back_populates='merchants')
    businesses = relationship('Business', back_populates='owner')

    def __str__(self):
        return f'{self.id}: {self.display_name}, {self.sub}'
