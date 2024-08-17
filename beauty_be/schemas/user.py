from pydantic import BaseModel
from pydantic import ConfigDict


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    display_name: str
    phone_number: str
