from pydantic import BaseModel


class BaseDBModel(BaseModel):
    """
    The base database model.
    """

    class Config:
        orm_mode = True
