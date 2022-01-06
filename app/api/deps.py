from typing import Generator

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.session import conn


def get_items_coll() -> Generator:
    try:
        db: AsyncIOMotorDatabase = conn.logistic_company_db
        coll = db.inventory
        yield coll
    finally:
        conn.close()
