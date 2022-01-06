from fastapi import APIRouter

from app.api.api_v1.endpoints import items

"""
Main API router of api_v1
"""
api_router = APIRouter()
api_router.include_router(items.router, prefix="/items", tags=["items"])
