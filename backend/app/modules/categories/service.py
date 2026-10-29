
from pymongo.asynchronous.database import AsyncDatabase

from app.modules.categories.repository import get_all_categories

from app.modules.categories.repository import (
    create_category,
    delete_category,
    get_all_categories,
    get_category_by_id,
    update_category,
)


async def list_categories(database: AsyncDatabase) -> list[dict]:
    """Возвращает список категорий для API."""

    return await get_all_categories(database)


async def add_category(
    database: AsyncDatabase,
    name: str,
) -> dict:
    """Проверяет название и создаёт пользовательскую категорию."""

    name = name.strip()

    if not name:
        raise ValueError("Название категории не может быть пустым")

    if len(name) > 100:
        raise ValueError("Название категории не должно превышать 100 символов")

    return await create_category(database, name)


async def rename_category(
    database: AsyncDatabase,
    category_id: str,
    name: str,
) -> dict:
    """Проверяет данные и переименовывает категорию."""

    name = name.strip()

    if not name:
        raise ValueError("Название категории не может быть пустым")

    if len(name) > 100:
        raise ValueError("Название категории не должно превышать 100 символов")

    category = await get_category_by_id(database, category_id)

    if category is None:
        raise LookupError("Категория не найдена")

    updated_category = await update_category(
        database,
        category_id,
        name,
    )

    if updated_category is None:
        raise LookupError("Категория не найдена")

    return updated_category


async def remove_category(
    database: AsyncDatabase,
    category_id: str,
) -> None:
    """Удаляет неиспользуемую пользовательскую категорию."""

    category = await get_category_by_id(database, category_id)

    if category is None:
        raise LookupError("Категория не найдена")

    if category["is_default"]:
        raise ValueError("Стандартную категорию нельзя удалить")

    transaction = await database.transactions.find_one(
        {"category_id": category["_id"]},
        {"_id": 1},
    )

    if transaction is not None:
        raise ValueError(
            "Категория используется в операциях. "
            "Сначала переназначьте эти операции на другую категорию."
        )

    deleted = await delete_category(database, category_id)

    if not deleted:
        raise LookupError("Категория не найдена")
