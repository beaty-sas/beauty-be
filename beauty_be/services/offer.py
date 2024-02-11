from typing import Sequence

from sqlalchemy import select

from beauty_be.services.base import BaseService
from beauty_models.beauty_models.models import Business
from beauty_models.beauty_models.models import Offer


class OfferService(BaseService[Offer]):
    MODEL = Offer

    async def get_by_business_id(self, business_id: int) -> Sequence[Offer]:
        query = select(self.MODEL).where(
            self.MODEL.businesses.any(Business.id == business_id),
        )
        return await self.fetch_all(query=query)

    async def get_by_ids(self, offer_ids: Sequence[int]) -> Sequence[Offer]:
        query = select(self.MODEL).where(
            self.MODEL.id.in_(offer_ids),
        )
        return await self.fetch_all(query=query)
