from beauty_be.services.base import BaseService
from beauty_models.beauty_models.models import Location


class LocationService(BaseService[Location]):
    MODEL = Location

    async def update_name(self, location_id: int, value: str) -> None:
        await self.update(
            filters=(self.MODEL.id == location_id,),
            values={'name': value},
        )
        await self.session.commit()
