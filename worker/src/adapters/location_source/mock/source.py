from random import randint
from typing import List

from domain.location import Location, LocationCreate
from port.location import ILocationSource


class MockLocationSource(ILocationSource):
    async def retrieve(self) -> List[LocationCreate]:
        res = []
        for _ in range(randint(1, 50_000)):
            try:
                res.append(self._get_location())
            except:
                continue
        return res

    def _get_location(self) -> LocationCreate:
        funcs = [
            self._get_location_v1,
            self._get_location_v2,
            self._get_location_v3,
        ]
        return funcs[randint(0, 2)]()

    def _get_location_v1(self):
        return LocationCreate(
            lac=randint(1, 1_000_000),
        )

    def _get_location_v2(self):
        return LocationCreate(
            eci=randint(1, 1_000_000),
        )

    def _get_location_v3(self):
        return LocationCreate(
            lac=randint(1, 1_000_000),
            cellid=randint(1, 1_000_000),
        )
