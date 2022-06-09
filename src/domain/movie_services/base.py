from db import MongoDb


class BaseService:
    def __init__(self, db: MongoDb):
        self.db = db

    async def add_document(self, data: dict):
        return await self.db.add(data)

    async def delete_document(self, id_: str):
        return await self.db.delete(id_)

    async def update_document(self, id_: str, data: dict):
        return await self.db.update(id_, data)
