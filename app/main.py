from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import uvicorn

from app.api.api_v1.api import api_router
from app.config import get_settings

settings = get_settings()
app = FastAPI(title=settings.APP_NAME)
app.include_router(api_router, prefix=f"{settings.API_V1_PREFIX}")


@app.exception_handler(ValueError)
@app.exception_handler(RequestValidationError)
async def value_error_exception_handler(request: Request, exc):
    """
    Custom Exception Handler
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(exc)}
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
