from datetime import datetime

from pydantic import BaseModel


class AvailableBookHourSchema(BaseModel):
    time: str

    class Config:
        from_attributes = True


class WorkingHoursBaseSchema(BaseModel):
    id: int
    date_from: datetime
    date_to: datetime

    class Config:
        from_attributes = True


class WorkingHoursCreateSchema(BaseModel):
    date_from: datetime
    date_to: datetime
