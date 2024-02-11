from pydantic import BaseModel

from beauty_be.schemas.attachment import AttachmentSchema
from beauty_be.schemas.location import LocationSchema


class BaseBusinessSchema(BaseModel):
    display_name: str
    phone_number: str

    class Config:
        from_attributes = True


class BusinessSchema(BaseBusinessSchema):
    location: LocationSchema | None
    logo: AttachmentSchema | None
