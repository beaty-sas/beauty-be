from pydantic import BaseModel


class LocationSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True
