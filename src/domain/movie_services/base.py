from typing import Union

from bson import ObjectId

from db import MongoDb


class BaseService:
    def __init__(self, db: MongoDb):
        self.db = db

    async def add_document(self, data: dict):
        return await self.db.add(data)

    async def delete_document(self, id_: Union[str, ObjectId]):
        return await self.db.delete(self.get_object_id(id_))

    async def update_document(self, id_: Union[str, ObjectId], data: dict):
        return await self.db.update(self.get_object_id(id_), data)

    async def get_document_by_id(self, id_: Union[str, ObjectId]):
        return await self.db.get_by_id(self.get_object_id(id_))

    @staticmethod
    def get_object_id(id_: Union[str, ObjectId]) -> ObjectId:
        if isinstance(id_, str):
            return ObjectId(id_)
        return id_
