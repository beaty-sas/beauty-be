from beauty_be.services.base import BaseService
from beauty_be.services.business import BusinessService
from beauty_models.beauty_models.models import Business
from beauty_models.beauty_models.models import Location


class LocationService(BaseService[Location]):
    MODEL = Location

    async def update_name(self, location_id: int, value: str) -> None:
        await self.update(
            filters=(self.MODEL.id == location_id,),
            values={'name': value},
        )
        await self.session.commit()

    async def update_or_create_name(self, business: Business, value: str) -> None:
        if business.location:
            await self.update_name(business.location.id, value)
            return

        business_service = BusinessService(self.session)
        location = await self.insert_obj(self.MODEL(name=value))
        await business_service.update(
            filters=(Business.id == business.id,),
            values={'location_id': location.id},
        )
        await self.session.commit()
