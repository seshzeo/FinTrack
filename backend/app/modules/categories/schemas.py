
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CategoryResponse(BaseModel):
    """Формат категории, который API возвращает клиенту."""

    id: str = Field(
        description="Уникальный идентификатор категории",
    )
    name: str = Field(
        min_length=1,
        max_length=100,
        description="Название категории",
    )
    is_default: bool = Field(
        description="Является ли категория стандартной",
    )
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        extra="forbid",
    )


class CategoryCreate(BaseModel):
    """Данные для создания пользовательской категории."""

    name: str = Field(
        min_length=1,
        max_length=100,
        description="Название новой категории",
    )

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )


class CategoryUpdate(BaseModel):
    """Данные для переименования категории."""

    name: str = Field(
        min_length=1,
        max_length=100,
        description="Новое название категории",
    )

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )
