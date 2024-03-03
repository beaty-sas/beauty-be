from pydantic import BaseModel


class AttachmentSchema(BaseModel):
    id: int
    original: str
    thumbnail: str

    class Config:
        from_attributes = True
