
from fastapi import APIRouter, Depends, HTTPException
from pymongo.asynchronous.database import AsyncDatabase

from app.db.mongo import get_database
from app.modules.categories.schemas import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.modules.categories.service import (
    add_category,
    list_categories,
    rename_category,
    remove_category,
)


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.get("", response_model=list[CategoryResponse])
async def get_categories(
    database: AsyncDatabase = Depends(get_database),
) -> list[CategoryResponse]:
    """Возвращает список всех категорий."""

    categories = await list_categories(database)

    return [
        CategoryResponse(
            id=str(category["_id"]),
            name=category["name"],
            is_default=category["is_default"],
            created_at=category["created_at"],
            updated_at=category["updated_at"],
        )
        for category in categories
    ]


@router.post("", response_model=CategoryResponse, status_code=201)
async def create_category(
    payload: CategoryCreate,
    database: AsyncDatabase = Depends(get_database),
) -> CategoryResponse:
    try:
        category = await add_category(database, payload.name)
    except ValueError as error:
        if "уже существует" in str(error):
            raise HTTPException(
                status_code=409,
                detail="Категория с таким названием уже существует",
            ) from error
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error
    
    return CategoryResponse(
        id=str(category["_id"]),
        name=category["name"],
        is_default=category["is_default"],
        created_at=category["created_at"],
        updated_at=category["updated_at"],
    )


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: str,
    payload: CategoryUpdate,
    database: AsyncDatabase = Depends(get_database),
) -> CategoryResponse:
    try:
        category = await rename_category(
            database,
            category_id,
            payload.name,
        )
    except LookupError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error
    except ValueError as error:
        if "уже существует" in str(error):
            raise HTTPException(
                status_code=409,
                detail=str(error),
            ) from error
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    return CategoryResponse(
        id=str(category["_id"]),
        name=category["name"],
        is_default=category["is_default"],
        created_at=category["created_at"],
        updated_at=category["updated_at"],
    )


@router.delete("/{category_id}", status_code=204)
async def delete_category(
    category_id: str,
    database: AsyncDatabase = Depends(get_database),
) -> None:
    try:
        await remove_category(database, category_id)
    except LookupError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error
    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error),
        ) from error