from pydantic import AnyHttpUrl
from pydantic import BaseModel
from pydantic import EmailStr


class Auth0UserSchema(BaseModel):
    sub: str | None
    name: str | None
    nickname: str | None
    picture: AnyHttpUrl | None
    email: EmailStr | None
    email_verified: bool | None
