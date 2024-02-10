from pydantic import BaseModel


class UserSchema(BaseModel):
    display_name: str
    phone_number: str

    class Config:
        from_attributes = True
