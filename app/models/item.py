from typing import Optional
from pydantic import Field, BaseModel

from app.models.OID import OID


class Item(BaseModel):
    id: Optional[OID]
    name: str = Field(...)
    brand: str = Field(...)
    quantity: int = Field(..., ge=0)
    supplier: str = Field(...)
