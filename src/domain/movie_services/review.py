from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from api.serializers import ReviewRatings
from db.mongodb import MongoDb, get_mongo_client
from domain.constants import MongoCollections
from domain.movie_services.base import BaseService
from domain.movie_services.pipelines import review_rating_pipeline


class ReviewService(BaseService):

    async def get_review_rating(self, movie_id: str, sorting: dict) -> ReviewRatings:
        aggr_pipeline = review_rating_pipeline(movie_id, sorting)
        result = await self.db.get_with_aggregation(aggr_pipeline)
        return ReviewRatings.parse_obj(result)


def get_review_service(
    mongo: AsyncIOMotorClient = Depends(get_mongo_client)
) -> ReviewService:
    mongodb = MongoDb(mongo, MongoCollections.review)
    return ReviewService(mongodb)
