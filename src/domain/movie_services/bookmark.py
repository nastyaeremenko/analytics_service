from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import parse_obj_as

from api.serializers import BookmarkOut
from db.mongodb import MongoDb, get_mongo_client
from domain.constants import MongoCollections
from domain.movie_services.base import BaseService


class BookmarkService(BaseService):

    async def get_bookmarks(self, user_id: str) -> list[BookmarkOut]:
        result = await self.db.get_all({'user_uuid': user_id})
        return parse_obj_as(list[BookmarkOut], result)


def get_bookmarks_service(
    mongo: AsyncIOMotorClient = Depends(get_mongo_client)
) -> BookmarkService:
    mongodb = MongoDb(mongo, MongoCollections.bookmarks)
    return BookmarkService(mongodb)
