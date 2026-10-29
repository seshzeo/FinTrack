
from datetime import datetime, timezone
from decimal import Decimal

from bson.decimal128 import Decimal128
from pymongo.asynchronous.database import AsyncDatabase


def _amount(value) -> Decimal:
    """Преобразует сумму из MongoDB в Decimal."""
    if isinstance(value, Decimal128):
        return value.to_decimal()
    return Decimal(str(value))


def _utc(value: datetime) -> datetime:
    """Приводит дату к UTC; дату без часового пояса считает UTC."""
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _iso(value: datetime | None) -> str | None:
    """Возвращает дату в формате ISO 8601."""
    return _utc(value).isoformat() if value is not None else None


async def get_statistics(
    database: AsyncDatabase,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> dict:
    """Считает общую статистику и распределение по категориям."""

    if date_from is not None:
        date_from = _utc(date_from)

    if date_to is not None:
        date_to = _utc(date_to)

    if (
        date_from is not None
        and date_to is not None
        and date_from > date_to
    ):
        raise ValueError(
            "Начальная дата не может быть позже конечной даты"
        )

    query = {}

    if date_from is not None or date_to is not None:
        query["date"] = {}

        if date_from is not None:
            query["date"]["$gte"] = date_from

        if date_to is not None:
            query["date"]["$lte"] = date_to

    cursor = database.transactions.find(query)
    documents = await cursor.to_list(length=None)

    # Загружаем категории одним запросом.
    category_ids = {
        document["category_id"]
        for document in documents
    }

    category_documents = await database.categories.find(
        {"_id": {"$in": list(category_ids)}}
    ).to_list(length=None)

    category_names = {
        category["_id"]: category["name"]
        for category in category_documents
    }

    total_income = Decimal("0.00")
    total_expense = Decimal("0.00")
    grouped: dict[str, dict] = {}

    for document in documents:
        category_id = document["category_id"]
        category_id_str = str(category_id)
        category_name = category_names.get(
            category_id,
            "Категория удалена",
        )
        amount = _amount(document["amount"])

        if category_id_str not in grouped:
            grouped[category_id_str] = {
                "category_id": category_id_str,
                "category_name": category_name,
                "income": Decimal("0.00"),
                "expense": Decimal("0.00"),
            }

        if document["type"] == "income":
            total_income += amount
            grouped[category_id_str]["income"] += amount
        else:
            total_expense += amount
            grouped[category_id_str]["expense"] += amount

    result_categories = []

    for item in grouped.values():
        income = item["income"]
        expense = item["expense"]

        result_categories.append(
            {
                "category_id": item["category_id"],
                "category_name": item["category_name"],
                "income": format(income, ".2f"),
                "expense": format(expense, ".2f"),
                "balance": format(income - expense, ".2f"),
            }
        )

    result_categories.sort(
        key=lambda item: Decimal(item["expense"]),
        reverse=True,
    )

    return {
        "date_from": _iso(date_from),
        "date_to": _iso(date_to),
        "total_income": format(total_income, ".2f"),
        "total_expense": format(total_expense, ".2f"),
        "balance": format(total_income - total_expense, ".2f"),
        "operations_count": len(documents),
        "categories": result_categories,
    }
