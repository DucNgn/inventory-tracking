from fastapi import HTTPException

def response(data, message: str) -> dict:
    return {"data": [data], "code": 200, "message": message}


def error_response(error: str, code: int, message: str):
    return {"error": error, "code": code, "message": message}
