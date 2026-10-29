from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from pymongo.asynchronous.database import AsyncDatabase

from app.db.mongo import get_database
from app.modules.transactions.schemas import (
    TransactionCreate,
    TransactionListResponse,
    TransactionResponse,
    TransactionUpdate,
)
from app.modules.transactions.service import (
    create_transaction,
    delete_transaction,
    get_transaction_item,
    list_transaction_items,
    update_transaction,
)

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("", response_model=TransactionListResponse)
async def get_transactions(
    type: str | None = Query(default=None, pattern="^(income|expense)$"),
    category_id: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    search: str | None = Query(default=None, max_length=100),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    database: AsyncDatabase = Depends(get_database),
):
    try:
        items, total = await list_transaction_items(
            database,
            transaction_type=type,
            category_id=category_id,
            date_from=date_from,
            date_to=date_to,
            search=search,
            limit=limit,
            offset=offset,
        )
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.post("", response_model=TransactionResponse, status_code=201)
async def create_transaction_endpoint(
    payload: TransactionCreate,
    database: AsyncDatabase = Depends(get_database),
):
    try:
        return await create_transaction(database, payload)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction_endpoint(
    transaction_id: str,
    database: AsyncDatabase = Depends(get_database),
):
    try:
        return await get_transaction_item(database, transaction_id)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction_endpoint(
    transaction_id: str,
    payload: TransactionUpdate,
    database: AsyncDatabase = Depends(get_database),
):
    try:
        return await update_transaction(database, transaction_id, payload)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.delete("/{transaction_id}", status_code=204)
async def delete_transaction_endpoint(
    transaction_id: str,
    database: AsyncDatabase = Depends(get_database),
) -> None:
    try:
        await delete_transaction(database, transaction_id)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
