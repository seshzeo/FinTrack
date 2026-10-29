
from bson import ObjectId
from datetime import datetime, timezone

from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError
from pymongo import ASCENDING
from pymongo.asynchronous.database import AsyncDatabase


async def get_all_categories(database: AsyncDatabase) -> list[dict]:
    """Возвращает все категории, сначала стандартные."""

    cursor = database.categories.find().sort(
        [
            ("is_default", -1),
            ("name_normalized", ASCENDING),
        ]
    )

    return await cursor.to_list(length=None)


async def create_category(
    database: AsyncDatabase,
    name: str,
) -> dict:
    """Создаёт пользовательскую категорию."""

    now = datetime.now(timezone.utc)

    category = {
        "name": name,
        "name_normalized": name.casefold(),
        "is_default": False,
        "default_key": None,
        "created_at": now,
        "updated_at": now,
    }

    try:
        result = await database.categories.insert_one(category)
    except DuplicateKeyError:
        raise ValueError("Категория с таким названием уже существует")

    created_category = await database.categories.find_one(
        {"_id": result.inserted_id}
    )

    if created_category is None:
        raise RuntimeError("Не удалось получить созданную категорию")

    return created_category


async def get_category_by_id(
    database: AsyncDatabase,
    category_id: str,
) -> dict | None:
    """Находит категорию по её MongoDB ID."""

    if not ObjectId.is_valid(category_id):
        return None

    return await database.categories.find_one(
        {"_id": ObjectId(category_id)}
    )


async def update_category(
    database: AsyncDatabase,
    category_id: str,
    name: str,
) -> dict | None:
    """Изменяет название существующей категории."""

    if not ObjectId.is_valid(category_id):
        return None

    now = datetime.now(timezone.utc)

    try:
        return await database.categories.find_one_and_update(
            {"_id": ObjectId(category_id)},
            {
                "$set": {
                    "name": name,
                    "name_normalized": name.casefold(),
                    "updated_at": now,
                }
            },
            return_document=ReturnDocument.AFTER,
        )
    except DuplicateKeyError:
        raise ValueError("Категория с таким названием уже существует")


async def delete_category(
    database: AsyncDatabase,
    category_id: str,
) -> bool:
    """Удаляет категорию по ID."""

    if not ObjectId.is_valid(category_id):
        return False

    result = await database.categories.delete_one(
        {
            "_id": ObjectId(category_id),
            "is_default": False,
        }
    )

    return result.deleted_count == 1
