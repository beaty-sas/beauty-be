from datetime import date
from datetime import datetime
from datetime import time

from pydantic import BaseModel


class AvailableBookHourSchema(BaseModel):
    time: datetime

    class Config:
        from_attributes = True


class WorkingHoursBaseSchema(BaseModel):
    id: int
    date: date
    opening_time: time
    closing_time: time

    class Config:
        from_attributes = True


class WorkingHoursCreateSchema(BaseModel):
    date: str
    opening_time: datetime
    closing_time: datetime
