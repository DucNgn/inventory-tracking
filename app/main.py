import uvicorn
from fastapi import FastAPI

from app.api.api_v1.api import api_router
from app.config import get_settings

settings = get_settings()
app = FastAPI(title=settings.APP_NAME)
app.include_router(api_router, prefix=f"{settings.API_V1_PREFIX}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
