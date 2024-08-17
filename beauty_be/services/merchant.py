from sqlalchemy.orm import selectinload

from beauty_be.clients.auth0 import auth0_client
from beauty_be.conf.constants import ErrorMessages
from beauty_be.exceptions import DoesNotExistError
from beauty_be.models.merchant import Merchant
from beauty_be.schemas.merchant import MerchantUpdateSchema
from beauty_be.services.base import BaseService


class MerchantService(BaseService[Merchant]):
    MODEL = Merchant

    async def get_by_sub(self, sub: str) -> Merchant | None:
        return await self.fetch_one(filters=(self.MODEL.sub == sub,))

    async def get_with_business(self, obj_id: int) -> Merchant:
        merchant = await self.fetch_one(
            filters=(self.MODEL.id == obj_id,), options=(selectinload(self.MODEL.businesses),)
        )
        if not merchant:
            raise DoesNotExistError(ErrorMessages.NOT_ENOUGH_PERMISSIONS)

        return merchant

    async def create(self, token: str, sub: str) -> Merchant:
        merchant_info = await auth0_client.get_user_info(token)
        merchant = self.MODEL(sub=sub, display_name=merchant_info.name)
        return await self.insert_obj(merchant)

    async def update_merchant(self, merchant: Merchant, data: MerchantUpdateSchema) -> Merchant:
        await self.update_obj(merchant, values=data.model_dump(exclude_unset=True))
        return await self.get_with_business(merchant.id)