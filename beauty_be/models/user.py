from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship

from beauty_be.models.base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    sub = Column(String(200), unique=True, nullable=True)
    display_name = Column(String(200), nullable=False)
    phone_number = Column(String(100), nullable=False, index=True)

    bookings = relationship('Booking', back_populates='user')

    def __str__(self):
        return f'{self.id}: {self.display_name}, {self.sub}'
