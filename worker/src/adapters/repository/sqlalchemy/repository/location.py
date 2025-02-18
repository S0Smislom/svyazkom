from typing import List

from adapters.repository.sqlalchemy.models.location import LocationModel
from domain.location import Location, LocationCreate
from port.location import ILocationRepository
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio.session import AsyncSession


class LocationRepository(ILocationRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, data: LocationCreate) -> Location:
        db_object = LocationModel(**data.model_dump(exclude_unset=True))
        self._session.add(db_object)
        await self._session.flush()
        return db_object.serialize()

    async def delete(self, item_id: int) -> None:
        stmt = delete(LocationModel).where(LocationModel.id == item_id)
        await self._session.execute(stmt)

    async def get_all(self) -> List[Location]:
        stmt = select(LocationModel)
        result = await self._session.execute(stmt)
        db_models = result.scalars().all()
        return [item.serialize() for item in db_models]

    async def bulk_create(self, data: List[Location]):
        if not data:
            return

        self._session.add_all(
            LocationModel(**item.model_dump(exclude_unset=True)) for item in data
        )
        await self._session.flush()

    async def bulk_remove(self, id_list: List[int]):
        if not id_list:
            return
        batch_size = 30000
        for i in range(0, len(id_list), batch_size):
            stmt = delete(LocationModel).where(
                LocationModel.id.in_(id_list[i : i + batch_size])
            )
            await self._session.execute(stmt)
