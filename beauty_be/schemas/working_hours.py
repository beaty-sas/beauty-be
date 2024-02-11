from datetime import datetime

from pydantic import BaseModel


class AvailableBookHourSchema(BaseModel):
    time: datetime

    class Config:
        from_attributes = True


class WorkingHoursBaseSchema(BaseModel):
    date: datetime
    opening_time: datetime
    closing_time: datetime

    class Config:
        from_attributes = True
