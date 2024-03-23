from enum import Enum

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import field_validator
from pydantic import SecretStr


class SocialProvider(str, Enum):
    GOOGLE: str = 'google-oauth2'
    FACEBOOK: str = 'facebook'
    APPLE: str = 'apple'


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str | None


class LoginRequestSchema(BaseModel):
    email: EmailStr
    password: SecretStr

    @field_validator('email')
    @classmethod
    def email_to_lower(cls, v: str) -> str:
        return v.lower()


class RegisterSocialResponseSchema(BaseModel):
    url: str


class RegisterSocialRequestSchema(BaseModel):
    redirect_url: str
    provider: SocialProvider
