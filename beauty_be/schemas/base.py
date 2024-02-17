from pydantic import BaseModel


class VersionSchema(BaseModel):
    version: str


class HealthSchema(BaseModel):
    db: bool
