from motor.motor_asyncio import AsyncIOMotorClient

from app.config import get_settings

settings = get_settings()
conn = AsyncIOMotorClient(settings.MONGO_URI)
