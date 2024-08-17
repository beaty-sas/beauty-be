from pydantic import BaseModel
from pydantic import ConfigDict

from beauty_be.schemas.attachment import AttachmentSchema
from beauty_be.schemas.location import LocationSchema


class BaseBusinessSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    display_name: str
    phone_number: str | None
    slug: str


class BusinessSchema(BaseBusinessSchema):
    location: LocationSchema | None
    logo: AttachmentSchema | None
    banner: AttachmentSchema | None


class UpdateBusinessSchema(BaseModel):
    display_name: str | None = None
    phone_number: str | None = None
    description: str | None = None
    logo_id: int | None = None
    banner_id: int | None = None
    location: LocationSchema | None = None
