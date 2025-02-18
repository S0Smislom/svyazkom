from abc import ABC, abstractmethod
from typing import List

from domain.location import Location, LocationCreate


class ILocationRepository(ABC):
    @abstractmethod
    async def create(self, data: LocationCreate) -> Location:
        pass

    @abstractmethod
    async def delete(self, item_id: int) -> None:
        pass

    @abstractmethod
    async def get_all(self) -> List[Location]:
        pass

    @abstractmethod
    async def bulk_create(self, data: List[Location]):
        pass

    @abstractmethod
    async def bulk_remove(self, id_list: List[int]):
        pass


class ILocationSource(ABC):
    @abstractmethod
    async def retrieve(self) -> List[LocationCreate]:
        pass


class ILocationService(ABC):
    @abstractmethod
    async def sync(self):
        pass
