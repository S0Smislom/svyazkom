import asyncio
import logging
import logging.config
import sys
from pathlib import Path

from adapters.location_source.http.source import HTTPLocationSource
from adapters.repository.sqlalchemy.repository.location import LocationRepository
from config.config import Config
from service.location import LocationService
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

BASE_DIR = Path(__file__).resolve().parent

logging.config.fileConfig(
    BASE_DIR / "config" / "logging.ini", disable_existing_loggers=False
)


logger = logging.getLogger()


class Worker:
    def __init__(self, config: Config):
        self.config = config
        engine = create_async_engine(config.DB_URL)
        self.session = async_sessionmaker(
            autocommit=False, autoflush=False, bind=engine
        )

    async def run(self):
        logger.info("Started")
        async with self.session() as session:
            try:
                await self._run(session)
                await session.commit()
            except Exception as e:
                logger.error(str(e))
                await session.rollback()

        logger.info("Finished")

    async def _run(self, session):
        repository = LocationRepository(session)
        source = HTTPLocationSource(
            self.config.SOURCE_URL,
            self.config.SOURCE_USERNAME,
            self.config.SOURCE_PASSWORD,
        )
        service = LocationService(
            location_repository=repository, location_source=source
        )
        await service.sync()


async def schedule(config: Config):
    worker = Worker(config)
    while True:
        asyncio.create_task(worker.run())
        await asyncio.sleep(config.INTERVAL)


def main():
    if len(sys.argv) < 2:
        logger.error(".env path not specified")
        return
    config = Config(_env_file=sys.argv[1], _env_file_encoding="utf-8")
    asyncio.run(schedule(config))


if __name__ == "__main__":
    main()
