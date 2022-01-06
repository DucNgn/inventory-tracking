from typing import Dict, Generic, Optional, TypeVar, Type, List, Union

from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.base import BaseDBModel

ModelType = TypeVar("ModelType", bound=BaseDBModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(
        self, db: AsyncIOMotorDatabase, obj_in: CreateSchemaType
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        operation = await db.insert_one(obj_in_data)
        new_record = await self.read(db=db, id=operation.inserted_id)
        return new_record

    async def read(self, db: AsyncIOMotorDatabase, id: str) -> Optional[ModelType]:
        res = await db.find_one({"_id": ObjectId(id)})
        if res:
            return self.model(**res, id=res["_id"])

    async def read_multi(self, db: AsyncIOMotorDatabase) -> List[ModelType]:
        res = []
        async for record in db.find():
            res.append(self.model(**record, id=record["_id"]))
        return res

    async def update(
        self,
        db: AsyncIOMotorDatabase,
        id: str,
        obj_in: Union[UpdateSchemaType, Dict[str, any]],
    ) -> Optional[ModelType]:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        ops = await db.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        updated_record = await self.read(db=db, id=id)
        return updated_record

    async def delete(self, db: AsyncIOMotorDatabase, id: str) -> ModelType:
        obj = await self.read(db, id)
        await db.delete_many({"_id": ObjectId(id)})
        return obj
