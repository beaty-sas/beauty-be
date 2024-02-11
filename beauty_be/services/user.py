from beauty_be.schemas.user import UserSchema
from beauty_be.services.base import BaseService
from beauty_models.beauty_models.models import User


class UserService(BaseService[User]):
    MODEL = User

    async def get_or_create_by_phone_number(self, user_data: UserSchema) -> User:
        if user := await self.fetch_one(filters=(self.MODEL.phone_number == user_data.phone_number,)):
            return user

        user = self.MODEL(phone_number=user_data.phone_number, display_name=user_data.display_name)
        return await self.insert_obj(user)
