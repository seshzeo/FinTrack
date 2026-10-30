
from datetime import datetime, timezone

from pymongo import ReturnDocument
from pymongo.asynchronous.database import AsyncDatabase


DEFAULT_CATEGORIES = [
    {
        "default_key": "salary",
        "name": "Зарплата",
    },
    {
        "default_key": "additional_income",
        "name": "Дополнительный доход",
    },
    {
        "default_key": "groceries",
        "name": "Продукты",
    },
    {
        "default_key": "transport",
        "name": "Транспорт",
    },
    {
        "default_key": "housing_utilities",
        "name": "Жильё и коммунальные услуги",
    },
    {
        "default_key": "health",
        "name": "Здоровье",
    },
    {
        "default_key": "entertainment",
        "name": "Развлечения",
    },
    {
        "default_key": "shopping",
        "name": "Покупки",
    },
    {
        "default_key": "other",
        "name": "Другое",
    },
]


async def seed_categories(database: AsyncDatabase) -> None:
    """Добавляет стандартные категории, если их ещё нет."""

    now = datetime.now(timezone.utc)

    for category in DEFAULT_CATEGORIES:
        await database.categories.find_one_and_update(
            {"default_key": category["default_key"]},
            {
                "$setOnInsert": {
                    **category,
                    "name_normalized": category["name"].casefold(),
                    "is_default": True,
                    "created_at": now,
                    "updated_at": now,
                }
            },
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )

    # Заполняем временные метки у ранее созданных категорий,
    # если они отсутствуют.
    await database.categories.update_many(
        {"created_at": {"$exists": False}},
        {"$set": {"created_at": now}},
    )

    await database.categories.update_many(
        {"updated_at": {"$exists": False}},
        {"$set": {"updated_at": now}},
    )
