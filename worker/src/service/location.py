import asyncio
import logging
from typing import List

from domain.location import Location, LocationCreate
from port.location import ILocationRepository, ILocationService, ILocationSource

logger = logging.getLogger()


class LocationService(ILocationService):
    def __init__(
        self,
        location_repository: ILocationRepository,
        location_source: ILocationSource,
    ):
        self.location_repository = location_repository
        self.location_source = location_source

    async def sync(self):
        # TODO optimize
        source_locations = await self._retrieve_from_source()
        db_locations = await self._retrieve_from_db()
        await asyncio.gather(
            self._add_records(source_locations, db_locations),
            self._remove_records(source_locations, db_locations),
        )

    async def _retrieve_from_source(self):
        res = await self.location_source.retrieve()
        logger.info(f"Retrieved from source: {len(res)}")
        return res

    async def _retrieve_from_db(self):
        res = await self.location_repository.get_all()
        logger.info(f"Retrieved from db: {len(res)}")
        return res

    async def _add_records(
        self, source_locations: List[LocationCreate], db_locations: List[Location]
    ):
        objects_to_add = []
        for item in source_locations:
            if not self._object_in(item, db_locations):
                objects_to_add.append(item)
        await self.location_repository.bulk_create(objects_to_add)
        logger.info(f"Created: {len(objects_to_add)}")

    async def _remove_records(
        self, source_locations: List[LocationCreate], db_locations: List[Location]
    ):
        objects_to_remove = []
        for item in db_locations:
            if not self._object_in(item, source_locations):
                objects_to_remove.append(item.id)
        await self.location_repository.bulk_remove(objects_to_remove)
        logger.info(f"Removed: {len(objects_to_remove)}")

    def _object_in(self, obj: LocationCreate, locations: List[LocationCreate]):
        for _ in locations:
            if obj.cellid == _.cellid and obj.eci == _.eci and obj.lac == _.lac:
                return True
        return False
