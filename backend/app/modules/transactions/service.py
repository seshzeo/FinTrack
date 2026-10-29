
from datetime import datetime, timezone
from decimal import Decimal

from bson import ObjectId
from bson.decimal128 import Decimal128
from pymongo.asynchronous.database import AsyncDatabase

from app.modules.transactions.repository import (
    get_transaction,
    insert_transaction,
    list_transactions,
    remove_transaction,
    replace_transaction,
)


def _to_utc(value: datetime) -> datetime:
    """Приводит дату к UTC; даты без часового пояса считает UTC."""
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _to_response_doc(document: dict, category: dict | None = None) -> dict:
    amount = document["amount"]

    if isinstance(amount, Decimal128):
        amount = amount.to_decimal()
    elif not isinstance(amount, Decimal):
        amount = Decimal(str(amount))

    return {
        "id": str(document["_id"]),
        "type": document["type"],
        "amount": format(amount, ".2f"),
        "category_id": str(document["category_id"]),
        "category_name": (
            category["name"] if category else "Категория удалена"
        ),
        "date": document["date"],
        "description": document.get("description"),
        "created_at": document["created_at"],
        "updated_at": document["updated_at"],
    }


async def _prepare_data(database: AsyncDatabase, payload) -> dict:
    if not ObjectId.is_valid(payload.category_id):
        raise LookupError("Категория не найдена")

    category = await database.categories.find_one(
        {"_id": ObjectId(payload.category_id)}
    )
    if category is None:
        raise LookupError("Категория не найдена")

    date = _to_utc(payload.date)
    now = datetime.now(timezone.utc)

    return {
        "type": payload.type,
        "amount": Decimal128(payload.amount),
        "category_id": category["_id"],
        "date": date,
        "description": payload.description,
        "updated_at": now,
    }


async def list_transaction_items(
    database: AsyncDatabase,
    *,
    transaction_type: str | None = None,
    category_id: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    search: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> tuple[list[dict], int]:
    if category_id and not ObjectId.is_valid(category_id):
        raise LookupError("Категория не найдена")

    if date_from is not None:
        date_from = _to_utc(date_from)

    if date_to is not None:
        date_to = _to_utc(date_to)

    if (
        date_from is not None
        and date_to is not None
        and date_from > date_to
    ):
        raise ValueError(
            "Начальная дата не может быть позже конечной даты"
        )

    documents, total = await list_transactions(
        database,
        transaction_type=transaction_type,
        category_id=category_id,
        date_from=date_from,
        date_to=date_to,
        search=search,
        limit=limit,
        offset=offset,
    )

    result = []
    for document in documents:
        category = await database.categories.find_one(
            {"_id": document["category_id"]}
        )
        result.append(_to_response_doc(document, category))

    return result, total


async def create_transaction(database: AsyncDatabase, payload) -> dict:
    data = await _prepare_data(database, payload)
    data["created_at"] = data["updated_at"]

    document = await insert_transaction(database, data)
    category = await database.categories.find_one(
        {"_id": document["category_id"]}
    )

    return _to_response_doc(document, category)


async def get_transaction_item(
    database: AsyncDatabase,
    transaction_id: str,
) -> dict:
    document = await get_transaction(database, transaction_id)

    if document is None:
        raise LookupError("Операция не найдена")

    category = await database.categories.find_one(
        {"_id": document["category_id"]}
    )

    return _to_response_doc(document, category)


async def update_transaction(
    database: AsyncDatabase,
    transaction_id: str,
    payload,
) -> dict:
    existing = await get_transaction(database, transaction_id)

    if existing is None:
        raise LookupError("Операция не найдена")

    data = await _prepare_data(database, payload)
    updated = await replace_transaction(
        database,
        transaction_id,
        data,
    )

    if updated is None:
        raise LookupError("Операция не найдена")

    category = await database.categories.find_one(
        {"_id": updated["category_id"]}
    )

    return _to_response_doc(updated, category)


async def delete_transaction(
    database: AsyncDatabase,
    transaction_id: str,
) -> None:
    deleted = await remove_transaction(database, transaction_id)

    if not deleted:
        raise LookupError("Операция не найдена")
