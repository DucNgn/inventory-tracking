import pandas as pd
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.crud.base import CRUDBase
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    async def get_csv(self, db: AsyncIOMotorDatabase) -> pd.DataFrame:
        all_records = []
        async for record in db.find():
            record["id"] = record.pop("_id")
            all_records.append(record)
        record_df = pd.DataFrame.from_dict(all_records)
        return record_df


item = CRUDItem(Item)
