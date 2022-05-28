from datetime import datetime
from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class MovieProgress(BaseOrjsonModel):
    movie_uuid: UUID
    movie_second: int
    movie_length: int
    current_date: datetime
