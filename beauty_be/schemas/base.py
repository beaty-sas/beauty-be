from pydantic import BaseModel


class VersionSchema(BaseModel):
    """Version response schema"""

    version: str


class HealthSchema(BaseModel):
    """Health response schema"""

    db: bool
