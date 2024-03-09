from pydantic import BaseModel


class BookingAnalyticSchema(BaseModel):
    total: int
    future: int
    today: int
