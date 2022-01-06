# MODELS

+ `OID.py` contains the FastAPI wrapper for ObjectID
+ `base.py` contains the base database model (BaseDBModel class). Only models that extend this class could have access to CRUD operation (see `app.crud.base.py`)
