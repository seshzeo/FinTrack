
import re
from datetime import datetime
from typing import Any

from bson import ObjectId
from pymongo import DESCENDING, ReturnDocument
from pymongo.asynchronous.database import AsyncDatabase


async def list_transactions(
    database: AsyncDatabase,
    *,
    transaction_type: str | None = None,
    category_id: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    search: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> tuple[list[dict[str, Any]], int]:
    query: dict[str, Any] = {}

    if transaction_type:
        query["type"] = transaction_type

    if category_id:
        query["category_id"] = ObjectId(category_id)

    if date_from is not None or date_to is not None:
        query["date"] = {}

        if date_from is not None:
            query["date"]["$gte"] = date_from

        if date_to is not None:
            query["date"]["$lte"] = date_to

    if search:
        query["description"] = {
            "$regex": re.escape(search),
            "$options": "i",
        }

    total = await database.transactions.count_documents(query)

    cursor = (
        database.transactions.find(query)
        .sort(
            [
                ("date", DESCENDING),
                ("created_at", DESCENDING),
            ]
        )
        .skip(offset)
        .limit(limit)
    )

    return await cursor.to_list(length=limit), total


async def get_transaction(
    database: AsyncDatabase,
    transaction_id: str,
) -> dict | None:
    if not ObjectId.is_valid(transaction_id):
        return None

    return await database.transactions.find_one(
        {"_id": ObjectId(transaction_id)}
    )


async def insert_transaction(
    database: AsyncDatabase,
    data: dict,
) -> dict:
    result = await database.transactions.insert_one(data)

    created = await database.transactions.find_one(
        {"_id": result.inserted_id}
    )

    if created is None:
        raise RuntimeError("Не удалось получить созданную операцию")

    return created


async def replace_transaction(
    database: AsyncDatabase,
    transaction_id: str,
    data: dict,
) -> dict | None:
    if not ObjectId.is_valid(transaction_id):
        return None

    return await database.transactions.find_one_and_update(
        {"_id": ObjectId(transaction_id)},
        {"$set": data},
        return_document=ReturnDocument.AFTER,
    )


async def remove_transaction(
    database: AsyncDatabase,
    transaction_id: str,
) -> bool:
    if not ObjectId.is_valid(transaction_id):
        return False

    result = await database.transactions.delete_one(
        {"_id": ObjectId(transaction_id)}
    )

    return result.deleted_count == 1
