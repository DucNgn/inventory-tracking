# CRUD

This directory contains the code for CRUD functionality as well as the extended operations on the database.

+ `base.py`: contains `CRUDBase` class. This is a generic class, allows for further extensible by other child classes.

    ```python
    # in base.py
    class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    ```

For example:

```python
# in crud_items.py
class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
```

Here, `CRUDItem` extends `CRUDBase` class and does 2 things:
+ assigns its own schemas (`Item`, `ItemCreate`, and `ItemUpdate`) to the generic fields.
+ extends with its own function:
    ```python
    async def get_csv(self, db: AsyncIOMotorDatabase)
    ```
