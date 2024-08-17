from pydantic import BaseModel
from pydantic import ConfigDict


class LocationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
