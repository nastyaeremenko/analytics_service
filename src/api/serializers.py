import datetime
from uuid import UUID

import orjson
from bson import ObjectId
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class BaseOrjsonModel(BaseModel):
    class Config:
        json_encoders = {ObjectId: str}
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class MovieProgress(BaseOrjsonModel):
    movie_uuid: UUID
    movie_progress: int
    movie_length: int


class MovieRating(BaseOrjsonModel):
    id: PyObjectId
    movie_uuid: UUID
    like: int
    dislike: int
    rating: float


class LikesModel(BaseOrjsonModel):
    like: int
    dislike: int


class ReviewRating(BaseOrjsonModel):
    id: PyObjectId = Field(..., alias='_id')
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


class BaseRateWithUserUUID(BaseOrjsonModel):
    def dict_with_user_uuid(self, user_uuid: str, *args, **kwargs):
        data = {}
        for key, value in self.dict(*args, **kwargs).items():
            if isinstance(value, UUID):
                value = str(value)
            elif isinstance(value, datetime.date):
                value = value.isoformat()
            data[key] = value
        data['user_uuid'] = user_uuid
        return data


class Bookmark(BaseRateWithUserUUID):
    movie_uuid: UUID


class BookmarkOut(Bookmark):
    id: PyObjectId = Field(..., alias='_id')


class RateMovie(BaseRateWithUserUUID):
    movie_uuid: UUID
    rating: int


class RateMovieOut(RateMovie):
    user_uuid: UUID
    id: PyObjectId = Field(..., alias='_id')


class Review(BaseRateWithUserUUID):
    movie_uuid: UUID
    text: str
    first_name: str
    last_name: str
    date: datetime.date
    rating: int


class ReviewOut(Review):
    id: PyObjectId = Field(..., alias='_id')
