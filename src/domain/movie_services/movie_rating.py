from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from api.serializers import MovieRating
from db.mongodb import MongoDb, get_mongo_client
from domain.constants import MongoCollections
from domain.movie_services.base import BaseService
from domain.movie_services.pipelines import movie_rating_pipeline


class MovieRatingService(BaseService):

    async def get_movie_rating(self, movie_id: str) -> MovieRating:
        aggr_pipeline = movie_rating_pipeline(movie_id)
        result = await self.db.get_with_aggregation(aggr_pipeline)
        return MovieRating.parse_obj(result[0])


def get_movie_rating_service(
    mongo: AsyncIOMotorClient = Depends(get_mongo_client)
) -> MovieRatingService:
    mongodb = MongoDb(mongo, MongoCollections.rating)
    return MovieRatingService(mongodb)
