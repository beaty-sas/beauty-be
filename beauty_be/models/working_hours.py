from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from beauty_be.models.base import BaseModel


class WorkingHours(BaseModel):
    __tablename__ = 'working_hours'

    date_from = Column(DateTime(timezone=True), nullable=False, index=True)
    date_to = Column(DateTime(timezone=True), nullable=False, index=True)

    business_id = Column(Integer, ForeignKey('businesses.id'), nullable=False)

    business = relationship('Business', back_populates='working_hours')

    def __str__(self):
        return f'{self.id}: {self.date_from} - {self.date_to}. Business: {self.business_id}'
