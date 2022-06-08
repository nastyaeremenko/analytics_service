from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient

from core.config import MONGO_DB


class MongoDb:
    def __init__(self, mongo_client: AsyncIOMotorClient, collection: str):
        self.collection = mongo_client[MONGO_DB][collection]

    async def get_all(self, id_: str) -> list:
        return await self.collection.find({"_id": id_}).to_list(length=None)

    async def get_with_aggregation(self, pipeline: list) -> list:
        return await self.collection.aggregate(pipeline).to_list(length=None)

    async def add(self, data: dict):
        return await self.collection.insert_one(data)

    async def delete(self, id_: str):
        return await self.collection.delete_one({"_id": id_})

    async def update(self, id_: str, data: dict):
        return await self.collection.replace_one({"_id": id_}, data)


mongo: Optional[AsyncIOMotorClient] = None


def get_mongo_client():
    return mongo
