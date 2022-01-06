from bson import ObjectId


class OID(str):
    """
    FastAPI Field Wrapper for Mongo ObjectID (see https://github.com/tiangolo/fastapi/issues/1515)
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if v == "":
            raise TypeError("ObjectId is empty")
        if ObjectId.is_valid(v) is False:
            raise TypeError("ObjectId invalid")
        return str(v)
