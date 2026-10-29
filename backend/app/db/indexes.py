from pymongo import ASCENDING, DESCENDING
from pymongo.asynchronous.database import AsyncDatabase


async def create_indexes(database: AsyncDatabase) -> None:
    """Создаёт индексы для коллекций FinTrack."""

    # Запрещаем повторение нормализованных названий категорий.
    await database.categories.create_index(
        [("name_normalized", ASCENDING)],
        unique=True,
        name="uq_categories_name_normalized",
    )

    # Ключ стандартной категории должен быть уникальным.
    # Пользовательские категории могут иметь default_key=None.
    await database.categories.create_index(
        [("default_key", ASCENDING)],
        unique=True,
        partialFilterExpression={
            "default_key": {"$type": "string"},
        },
        name="uq_categories_default_key",
    )

    # Сортировка операций по дате и времени создания.
    await database.transactions.create_index(
        [
            ("date", DESCENDING),
            ("created_at", DESCENDING),
        ],
        name="ix_transactions_date_created",
    )

    # Фильтрация операций по типу и периоду.
    await database.transactions.create_index(
        [
            ("type", ASCENDING),
            ("date", DESCENDING),
            ("created_at", DESCENDING),
        ],
        name="ix_transactions_type_date_created",
    )

    # Фильтрация операций по категории и дате.
    await database.transactions.create_index(
        [
            ("category_id", ASCENDING),
            ("date", DESCENDING),
        ],
        name="ix_transactions_category_date",
    )