from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get(
    "/",
    response_model=List[schemas.Item],
    response_description="Get a list of all items in inventory",
)
async def all_items(db: AsyncIOMotorDatabase = Depends(deps.get_db)) -> Any:
    items = await crud.item.read_multi(db)
    return items


@router.get(
    "/{id}", response_model=schemas.Item, response_description="Get an item info by ID"
)
async def get_item_by_id(
    id: str, db: AsyncIOMotorDatabase = Depends(deps.get_db)
) -> Any:
    retrived_item = await crud.item.read(db=db, id=id)
    if not retrived_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return retrived_item


@router.post(
    "/", response_model=schemas.Item, response_description="The newly created item"
)
async def create_item(
    new_item: schemas.ItemCreate, db: AsyncIOMotorDatabase = Depends(deps.get_db)
) -> Any:
    item = await crud.item.create(db=db, obj_in=new_item)
    return item


@router.put(
    "/{id}", response_model=schemas.Item, response_description="The updated item"
)
async def update_item(
    id: str,
    item_in: schemas.ItemUpdate,
    db: AsyncIOMotorDatabase = Depends(deps.get_db),
) -> Any:
    retrived_item = await crud.item.read(db=db, id=id)
    if not retrived_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    updated_item = await crud.item.update(db=db, id=id, obj_in=item_in)
    return updated_item


@router.delete("/{id}", response_model=schemas.Item)
async def delete_item(id: str, db: AsyncIOMotorDatabase = Depends(deps.get_db)) -> Any:
    retrived_item = await crud.item.read(db=db, id=id)
    if not retrived_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    item = await crud.item.delete(db=db, id=id)
    return item
