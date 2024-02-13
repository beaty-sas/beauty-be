from pydantic import BaseModel


class MerchantSchema(BaseModel):
    sub: str
    display_name: str
    phone_number: str
    logo_id: int | None

    class Config:
        from_attributes = True


class MerchantUpdateSchema(BaseModel):
    display_name: str
    phone_number: str
    logo_id: int | None

    class Config:
        from_attributes = True
