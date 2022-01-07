from typing import Generator
import asyncio

import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi.testclient import TestClient

from app.main import app
from app.config import get_settings
from app.db.session import conn

"""
All fixtures to be applied to pytest
"""


@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop()
    conn.io_loop = loop
    yield loop


@pytest.fixture(scope="session")
def db() -> Generator:
    settings = get_settings()
    db: AsyncIOMotorDatabase = conn.logistic_company_db
    coll = db.get_collection(settings.TEST_COLLECTION)
    yield coll
    db.drop_collection(coll)


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app=app) as client:
        yield client
