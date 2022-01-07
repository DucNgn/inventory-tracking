import pandas as pd
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.crud.base import CRUDBase
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate, ItemOID


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate, ItemOID]):
    async def get_all_items_dataframe(self, db: AsyncIOMotorDatabase) -> pd.DataFrame:
        """
        Extract a pandas dataframe of all items in the inventory

        Parameters
        ----------
        :db the database collection

        Returns
        -------
        :return a Pandas dataframe of all items
        """
        all_records = []
        async for record in db.find():
            record["id"] = record.pop("_id")
            all_records.append(record)
        record_df = pd.DataFrame.from_dict(all_records)
        return record_df


item = CRUDItem(Item)
