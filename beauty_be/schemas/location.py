from pydantic import BaseModel


class LocationSchema(BaseModel):
    name: str
    geom: str | None

    class Config:
        from_attributes = True
