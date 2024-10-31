# from asyncio import get_event_loop_policy
# from os import environ
# from types import SimpleNamespace
# from uuid import uuid4
from fastapi.testclient import TestClient
import pytest
from aiohttp.test_utils import TestClient
from httpx import AsyncClient
# from app.settings import get_settings
# from app.db.connection import SessionManager

from app.__main__ import app

import pytest


@pytest.fixture
def test_user():
    json = {
        "username": "kitty",
        "password": "secret12345",
        "email": "kitty@mail.ru"
    }
    return json


@pytest.fixture
def client() -> AsyncClient:
    """
    Returns a client that can be used to interact with the application.
    """
    yield AsyncClient(app=app, base_url="http://test")
