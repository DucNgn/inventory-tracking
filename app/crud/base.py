from typing import Dict, Generic, Optional, TypeVar, Type, List, Union

from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(
        self, db: AsyncIOMotorDatabase, obj_in: CreateSchemaType
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        new_obj = await db.insert_one(obj_in_data)
        new_record = await self.read(db=db, id=new_obj.inserted_id)
        return new_record

    async def read(self, db: AsyncIOMotorDatabase, id: str) -> Optional[ModelType]:
        res = await db.find_one({"_id": ObjectId(id)})
        if res:
            return res

    async def read_multi(self, db: AsyncIOMotorDatabase) -> List[ModelType]:
        res = []
        async for record in db.find():
            res.append(record)
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

        updated_record = await db.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )
        if updated_record:
            return True
        return False

    async def delete(self, db: AsyncIOMotorDatabase, id: str) -> ModelType:
        obj = await self.read(db, id)
        await db.delete_many({"_id": ObjectId(id)})
        return obj
