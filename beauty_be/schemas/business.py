from pydantic import BaseModel

from beauty_be.schemas.attachment import AttachmentSchema
from beauty_be.schemas.location import LocationSchema


class BaseBusinessSchema(BaseModel):
    id: int
    display_name: str
    phone_number: str | None
    slug: str

    class Config:
        from_attributes = True


class BusinessSchema(BaseBusinessSchema):
    location: LocationSchema | None
    logo: AttachmentSchema | None
    banner: AttachmentSchema | None


class UpdateBusinessSchema(BaseModel):
    display_name: str
    phone_number: str
    description: str | None = None
    logo_id: int | None = None
    banner_id: int | None = None
    location: LocationSchema
