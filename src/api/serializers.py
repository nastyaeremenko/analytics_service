import datetime
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
    movie_progress: int
    movie_length: int


class MovieRating(BaseOrjsonModel):
    movie_uuid: UUID
    like: int
    dislike: int
    rating: float


class LikesModel(BaseOrjsonModel):
    like: int
    dislike: int


class ReviewRating(BaseOrjsonModel):
    movie_uuid: UUID
    user_uuid: UUID
    text: str
    first_name: str
    last_name: str
    date: datetime.date
    rating: int
    ratings: list[LikesModel]


class ReviewRatings(BaseOrjsonModel):
    __root__: list[ReviewRating]
