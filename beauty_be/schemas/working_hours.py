from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class AvailableBookHourSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    time: str


class WorkingHoursBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date_from: datetime
    date_to: datetime


class WorkingHoursCreateSchema(BaseModel):
    date_from: datetime
    date_to: datetime
