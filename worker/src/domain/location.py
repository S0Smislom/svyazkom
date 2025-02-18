from typing import Optional

from pydantic import BaseModel, Field, model_validator


class Location(BaseModel):
    id: int
    lac: Optional[int] = None
    cellid: Optional[int] = None
    eci: Optional[int] = None
    note: Optional[str] = None


class LocationCreate(BaseModel):
    lac: Optional[int] = Field(None, gt=0, lt=65535)
    cellid: Optional[int] = Field(None, gt=0, lt=65535)
    eci: Optional[int] = Field(None, gt=0, lt=268435455)
    note: Optional[str] = Field(None, max_length=200)

    @model_validator(mode="after")
    def check_fields(self):
        if self.lac and not self.cellid and not self.eci:
            return self
        if self.lac and self.cellid and not self.eci:
            return self
        if not self.lac and not self.cellid and self.eci:
            return self
        raise ValueError("lac or lac+cellid or eci")
