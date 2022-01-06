from pydantic import BaseModel


class BaseDBModel(BaseModel):
    class Config:
        orm_mode = True
