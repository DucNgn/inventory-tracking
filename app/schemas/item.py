from typing import Optional

from pydantic import BaseModel

# Base Item Class
class ItemBase(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    supplier: Optional[str] = None
    quantity: Optional[int] = 0


# Properties must receive when creating new item
class ItemCreate(ItemBase):
    name: str
    brand: str
    supplier: str


# Properties must receive when getting new item
class ItemUpdate(ItemBase):
    pass


# Properties stored in DB
class ItemInDBBase(ItemBase):
    id: str
    name: str
    brand: str
    supplier: str
    quantity: int


# Properties must return to client
class Item(ItemInDBBase):
    pass
