from typing import Optional

from pydantic import Field

from app.models.OID import OID
from app.models.base import BaseDBModel


class Item(BaseDBModel):
    """
    Item stored in the database.
    """

    id: Optional[OID]
    name: str = Field(...)
    brand: str = Field(...)
    quantity: int = Field(..., ge=0)
    supplier: str = Field(...)
