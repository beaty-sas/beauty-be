from datetime import datetime

from pydantic import BaseModel


class AvailableBookHourSchema(BaseModel):
    time: datetime

    class Config:
        from_attributes = True
