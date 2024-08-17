from pydantic import BaseModel
from pydantic import ConfigDict

from beauty_be.schemas.business import BaseBusinessSchema


class MerchantSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sub: str
    display_name: str | None
    phone_number: str | None
    logo_id: int | None
    businesses: list[BaseBusinessSchema]


class MerchantUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    display_name: str | None = None
    phone_number: str | None = None
    logo_id: int | None = None
    telegram_id: str | None = None
