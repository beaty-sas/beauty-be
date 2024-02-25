from pydantic import BaseModel

from beauty_be.schemas.attachment import AttachmentSchema
from beauty_be.schemas.location import LocationSchema


class BaseBusinessSchema(BaseModel):
    id: int
    display_name: str
    phone_number: str

    class Config:
        from_attributes = True


class BusinessSchema(BaseBusinessSchema):
    location: LocationSchema | None
    logo: AttachmentSchema | None


class UpdateBusinessSchema(BaseModel):
    display_name: str
    phone_number: str
    logo_id: int | None = None
    location: LocationSchema
