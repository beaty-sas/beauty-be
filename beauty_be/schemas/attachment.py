from pydantic import BaseModel
from pydantic import ConfigDict


class AttachmentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    original: str
    thumbnail: str
