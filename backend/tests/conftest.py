import os

# ВАЖНО: до импорта app, чтобы settings прочитал тестовую БД.
# CORS_ORIGINS НЕ задаём — пусть читается из .env (иначе pydantic-settings
# падает на парсинге list[str] из плоской строки).
os.environ["MONGODB_DATABASE"] = "fintrack_test"
os.environ["MONGODB_URI"] = "mongodb://127.0.0.1:27017"

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager

from app.main import app
from app.db import mongo as mongo_module


def _get_db():
    """Достаём Database из модуля mongo, не завязываясь на конкретное имя."""
    for attr in ("db", "database"):
        obj = getattr(mongo_module, attr, None)
        if obj is not None:
            return obj
    for attr in ("get_database", "get_db"):
        fn = getattr(mongo_module, attr, None)
        if callable(fn):
            return fn()
    raise RuntimeError("Не нашли Database в app.db.mongo — поправьте _get_db()")


@pytest_asyncio.fixture(scope="session")
async def client():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac


@pytest_asyncio.fixture(autouse=True)
async def clean_db(client):
    """Чистим коллекции перед каждым тестом. Стандартные категории из lifespan
    тоже удаляются — тесты начинают с пустой БД."""
    db = _get_db()
    if db.name != "fintrack_test":
        raise RuntimeError(
            f"Тесты остановлены: недопустимая база данных '{db.name}'"
        )
    
    await db.categories.delete_many({})
    await db.transactions.delete_many({})
    yield