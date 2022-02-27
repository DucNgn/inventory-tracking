from typing import Dict, Generic, Optional, TypeVar, Type, List, Union
from bson.objectid import ObjectId
from bson.errors import InvalidId

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.base import BaseDBModel
from app.schemas.OID import BaseOID

ModelType = TypeVar("ModelType", bound=BaseDBModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
IDSchemaType = TypeVar("IDSchemaType", bound=BaseOID)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType, IDSchemaType]):
    """
    The generic base class for all CRUD operations.
    Child Classes inherit this CRUDBase has instant access to CRUD operations.

    :ModelType The model from database (must be derived from app.models.base.BaseDBModel)
    :CreateSchemaType The schema for creating new object
    :UpdateSchemaType The schema for updating an object
    :IDSchemaType The schema of the Object ID
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(
        self, db: AsyncIOMotorDatabase, obj_in: CreateSchemaType
    ) -> ModelType:
        """
        Create a new object of ModelType in the database.

        Parameters
        ----------
        :db the database collection
        :obj_in new object to create, must of CreateSchemaType schema

        Returns
        -------
        :return the newly created object
        """
        obj_in_data = jsonable_encoder(obj_in)
        operation = await db.insert_one(obj_in_data)
        new_record = await self.read_by_id(db=db, id=operation.inserted_id)
        return new_record

    async def read_by_id(
        self, db: AsyncIOMotorDatabase, id: Union[IDSchemaType, str]
    ) -> Optional[ModelType]:
        """
        Retrive a record in the database by ID.

        Parameters
        ----------
        :db the database collection
        :id the object id of the record to be retrieved

        Returns
        -------
        :return the retrieved object, None if not found.
        """
        if isinstance(id, str):
            try:
                id = ObjectId(id)
            except InvalidId:
                raise ValueError("Invalid ID")

        res = await db.find_one({"_id": id})
        if res:
            return self.model(**res, id=res["_id"])

    async def read_all(self, db: AsyncIOMotorDatabase) -> List[ModelType]:
        """
        Retrive all records in the database.

        Parameters
        ----------
        :db the database collection

        Returns
        -------
        :return a list of records (ModelType) in the collection
        """
        res = []
        async for record in db.find():
            res.append(self.model(**record, id=record["_id"]))
        return res

    async def update(
        self,
        db: AsyncIOMotorDatabase,
        id: Union[IDSchemaType, str],
        obj_in: Union[UpdateSchemaType, Dict[str, any]],
    ) -> Optional[ModelType]:
        """
        Update a record in the database by id.

        Parameters
        ----------
        :db the database collection
        :id the object ID of the record to be updated
        :obj_in the updated data for the record.

        Returns
        -------
        :return the updated record, None if not found
        """
        if isinstance(id, str):
            try:
                id = ObjectId(id)
            except InvalidId:
                raise ValueError("Invalid ID")

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        await db.update_one({"_id": id}, {"$set": update_data})
        updated_record = await self.read_by_id(db=db, id=id)
        return updated_record

    async def delete(
        self, db: AsyncIOMotorDatabase, id: Union[IDSchemaType, str]
    ) -> Optional[ModelType]:
        """
        Delete a record in the database by id.

        Parameters
        ----------
        :db the database collection
        :id the object ID of the record to be deleted

        Returns
        -------
        :return the deleted record, None if not found
        """
        if isinstance(id, str):
            try:
                id = ObjectId(id)
            except InvalidId:
                raise ValueError("Invalid ID")

        obj = await self.read_by_id(db=db, id=id)
        await db.delete_many({"_id": ObjectId(id)})
        return obj
