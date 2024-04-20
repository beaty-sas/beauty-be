from pydantic import BaseModel

from beauty_be.schemas.attachment import AttachmentSchema
from beauty_be.schemas.location import LocationSchema


class MerchantSchema(BaseModel):
    sub: str
    display_name: str | None
    phone_number: str | None
    logo: AttachmentSchema | None
    banner: AttachmentSchema | None
    location: LocationSchema | None

    class Config:
        from_attributes = True


class MerchantUpdateSchema(BaseModel):
    display_name: str
    phone_number: str
    logo_id: int | None

    class Config:
        from_attributes = True
