from beauty_be.clients.auth0 import auth0_client
from beauty_be.schemas.merchant import MerchantUpdateSchema
from beauty_be.services.base import BaseService
from beauty_models.beauty_models.models import Merchant


class MerchantService(BaseService[Merchant]):
    MODEL = Merchant

    async def get_by_sub(self, sub: str) -> Merchant | None:
        return await self.fetch_one(filters=(self.MODEL.sub == sub,))

    async def create(self, token: str, sub: str) -> Merchant:
        merchant_info = await auth0_client.get_user_info(token)
        merchant = self.MODEL(sub=sub, display_name=merchant_info.name)
        return await self.insert_obj(merchant)

    async def update_merchant(self, merchant: Merchant, data: MerchantUpdateSchema) -> Merchant:
        return await self.update_obj(merchant, values=data.dict(exclude_unset=True))
