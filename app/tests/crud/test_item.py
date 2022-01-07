import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase

from app import crud
from app.schemas.item import ItemCreate, ItemUpdate


@pytest.mark.asyncio
async def test_create_item(db: AsyncIOMotorDatabase) -> None:
    name = "Skateboard"
    brand = "Snowdevil"
    supplier = "Shopify"

    new_item = ItemCreate(
        name=name,
        brand=brand,
        supplier=supplier,
    )
    item = await crud.item.create(db=db, obj_in=new_item)
    assert item.name == name
    assert item.brand == brand
    assert item.supplier == supplier
    assert item.quantity == 0  # default quantity


@pytest.mark.asyncio
async def test_read_item_by_id(db: AsyncIOMotorDatabase) -> None:
    name = "Phone"
    brand = "Fruit"
    supplier = "BestBuy"
    quantity = 15

    new_item = ItemCreate(name=name, brand=brand, supplier=supplier, quantity=quantity)
    item = await crud.item.create(db, obj_in=new_item)
    retrived_item = await crud.item.read_by_id(db=db, id=item.id)
    assert retrived_item.name == name
    assert retrived_item.brand == brand
    assert retrived_item.supplier == supplier
    assert retrived_item.quantity == quantity


@pytest.mark.asyncio
async def test_update_item_by_id(db: AsyncIOMotorDatabase) -> None:
    name = "Headphone"
    brand = "Sony"
    supplier = "local-electronic"
    quantity = 1

    new_item = ItemCreate(name=name, brand=brand, supplier=supplier, quantity=quantity)
    item = await crud.item.create(db, obj_in=new_item)

    new_supplier = "Walmart"
    update_obj = ItemUpdate(supplier=new_supplier)
    updated_item = await crud.item.update(db=db, id=item.id, obj_in=update_obj)

    assert updated_item.name == name
    assert updated_item.brand == brand
    assert updated_item.supplier == new_supplier
    assert updated_item.quantity == quantity


@pytest.mark.asyncio
async def test_delete_item_by_id(db: AsyncIOMotorDatabase) -> None:
    name = "Laptop"
    brand = "Acer"
    supplier = "local-electronic"
    quantity = 0

    new_item = ItemCreate(name=name, brand=brand, supplier=supplier, quantity=quantity)
    item = await crud.item.create(db=db, obj_in=new_item)
    deleted_item = await crud.item.delete(db=db, id=item.id)
    retrieved_item = await crud.item.read_by_id(db=db, id=item.id)

    assert retrieved_item is None
    assert deleted_item.name == name
    assert deleted_item.brand == brand
    assert deleted_item.supplier == supplier
    assert deleted_item.quantity == quantity
