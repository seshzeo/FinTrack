from datetime import datetime, timezone
from decimal import Decimal

from bson.decimal128 import Decimal128
from pymongo.asynchronous.database import AsyncDatabase


def _amount(value) -> Decimal:
    if isinstance(value, Decimal128):
        return value.to_decimal()
    return Decimal(str(value))


async def get_statistics(
    database: AsyncDatabase,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> dict:
    if date_from and date_to and date_from > date_to:
        raise ValueError("Начальная дата не может быть позже конечной даты")
    query = {}
    if date_from or date_to:
        query["date"] = {}
        if date_from:
            query["date"]["$gte"] = _utc(date_from)
        if date_to:
            query["date"]["$lte"] = _utc(date_to)

    cursor = database.transactions.find(query)
    documents = await cursor.to_list(length=None)
    total_income = Decimal("0.00")
    total_expense = Decimal("0.00")
    grouped: dict[str, dict] = {}

    for doc in documents:
        category_id = str(doc["category_id"])
        category = await database.categories.find_one({"_id": doc["category_id"]})
        name = category["name"] if category else "Категория удалена"
        amount = _amount(doc["amount"])
        if category_id not in grouped:
            grouped[category_id] = {
                "category_id": category_id,
                "category_name": name,
                "income": Decimal("0.00"),
                "expense": Decimal("0.00"),
            }
        if doc["type"] == "income":
            total_income += amount
            grouped[category_id]["income"] += amount
        else:
            total_expense += amount
            grouped[category_id]["expense"] += amount

    categories = []
    for item in grouped.values():
        categories.append({
            "category_id": item["category_id"],
            "category_name": item["category_name"],
            "income": format(item["income"], ".2f"),
            "expense": format(item["expense"], ".2f"),
            "balance": format(item["income"] - item["expense"], ".2f"),
        })
    categories.sort(key=lambda item: Decimal(item["expense"]), reverse=True)

    return {
        "date_from": _iso(date_from),
        "date_to": _iso(date_to),
        "total_income": format(total_income, ".2f"),
        "total_expense": format(total_expense, ".2f"),
        "balance": format(total_income - total_expense, ".2f"),
        "operations_count": len(documents),
        "categories": categories,
    }


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _iso(value: datetime | None) -> str | None:
    return _utc(value).isoformat() if value else None
