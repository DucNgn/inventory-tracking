from typing import Generator

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.session import conn


def get_items_coll() -> Generator:
    """
    This function serves as a dependency to generate database collection from MongoDB
    """
    try:
        db: AsyncIOMotorDatabase = conn.logistic_company_db
        coll = db.inventory
        yield coll
    finally:
        conn.close()
