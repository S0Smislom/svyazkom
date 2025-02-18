from domain.location import Location
from sqlalchemy import CheckConstraint, Column, Integer, String

from .base import Base


class LocationModel(Base):
    __tablename__ = "location"

    __table_args__ = (
        CheckConstraint(
            "(lac is not null and eci is null) or (lac is null and cellid is null and eci is not null)"
        ),
    )

    id = Column(Integer, primary_key=True)
    lac = Column(Integer, nullable=True)
    cellid = Column(Integer, nullable=True)
    eci = Column(Integer, nullable=True)
    note = Column(String(200), nullable=True)

    def serialize(self) -> Location:
        return Location(
            id=self.id,
            lac=self.lac,
            cellid=self.cellid,
            eci=self.eci,
            note=self.note,
        )
