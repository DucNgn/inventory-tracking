from motor.motor_asyncio import AsyncIOMotorClient

from app.config import get_settings

"""
Setup a connection with the Mongo Database
"""
settings = get_settings()
conn = AsyncIOMotorClient(settings.MONGO_URI)
