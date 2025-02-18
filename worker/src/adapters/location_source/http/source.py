import logging
from base64 import b64encode
from typing import List

import aiohttp
from domain.location import Location, LocationCreate
from port.location import ILocationSource

logger = logging.getLogger()


class HTTPLocationSource(ILocationSource):

    def __init__(self, url: str, username: str = None, password: str = None):
        self.url = url
        self.basic_auth = (
            self._basic_auth(username, password) if username and password else None
        )

    async def retrieve(self):
        data = await self._get()
        return self._serialize(data)

    def _serialize(self, data: list) -> List[LocationCreate]:
        res = []
        for _ in data:
            try:
                res.append(LocationCreate(**_))
            except:
                pass
        return res

    async def _get(self):
        logger.info("Requested locations from source")

        async with aiohttp.ClientSession(raise_for_status=True) as session:
            headers = self._headers()
            async with session.get(self.url, headers=headers) as response:
                return await response.json()

    def _headers(self):
        headers = {}
        if self.basic_auth:
            headers.update({"Authorization": self.basic_auth})
        return headers

    def _basic_auth(self, username: str, password: str):
        token = b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
        return f"Basic {token}"
