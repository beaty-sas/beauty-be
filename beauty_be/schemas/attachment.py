from pydantic import BaseModel


class AttachmentSchema(BaseModel):
    original: str
    thumbnail: str

    class Config:
        from_attributes = True
