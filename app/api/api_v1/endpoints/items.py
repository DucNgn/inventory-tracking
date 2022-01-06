from typing import Any, List
import io

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorDatabase

from app import crud, schemas
from app.api import deps

"""
APIs to interact with Items
"""
router = APIRouter()


@router.get(
    "/",
    response_model=List[schemas.Item],
    response_description="Get a list of all items in inventory",
)
async def all_items(db: AsyncIOMotorDatabase = Depends(deps.get_items_coll)) -> Any:
    items = await crud.item.read_all(db)
    return items


@router.get(
    "/get_csv",
    response_class=StreamingResponse,
    response_description="Get a .csv file of the inventory",
)
async def get_csv(db: AsyncIOMotorDatabase = Depends(deps.get_items_coll)) -> Any:
    record_df = await crud.item.get_all_items_dataframe(db=db)
    stream = io.StringIO()
    record_df.to_csv(stream, index=False)
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=inventory.csv"
    return response


@router.get(
    "/{id}",
    response_model=schemas.Item,
    response_description="Get an item info by ID",
)
async def get_item_by_id(
    id: str, db: AsyncIOMotorDatabase = Depends(deps.get_items_coll)
) -> Any:
    retrived_item = await crud.item.read_by_id(db=db, id=id)
    if not retrived_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Requested item not found"
        )
    return retrived_item


@router.post(
    "/",
    response_model=schemas.Item,
    response_description="The newly created item",
)
async def create_item(
    new_item: schemas.ItemCreate,
    db: AsyncIOMotorDatabase = Depends(deps.get_items_coll),
) -> Any:
    item = await crud.item.create(db=db, obj_in=new_item)
    return item


@router.put(
    "/{id}",
    response_model=schemas.Item,
    response_description="The updated item",
)
async def update_item_by_id(
    id: str,
    item_in: schemas.ItemUpdate,
    db: AsyncIOMotorDatabase = Depends(deps.get_items_coll),
) -> Any:
    retrived_item = await crud.item.read_by_id(db=db, id=id)
    if not retrived_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Requested item not found"
        )
    updated_item = await crud.item.update(db=db, id=id, obj_in=item_in)
    return updated_item


@router.delete(
    "/{id}",
    response_model=schemas.Item,
    response_description="The item just got deleted",
)
async def delete_item_by_id(
    id: str, db: AsyncIOMotorDatabase = Depends(deps.get_items_coll)
) -> Any:
    retrived_item = await crud.item.read_by_id(db=db, id=id)
    if not retrived_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Requested item not found"
        )
    item = await crud.item.delete(db=db, id=id)
    return item
