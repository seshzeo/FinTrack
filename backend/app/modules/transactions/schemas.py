from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


TransactionType = Literal["income", "expense"]


class TransactionCreate(BaseModel):
    type: TransactionType
    amount: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    category_id: str
    date: datetime
    description: str | None = Field(default=None, max_length=500)

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    @field_validator("description")
    @classmethod
    def empty_description_to_none(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            return None
        return value


class TransactionUpdate(BaseModel):
    type: TransactionType
    amount: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    category_id: str
    date: datetime
    description: str | None = Field(default=None, max_length=500)

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    @field_validator("description")
    @classmethod
    def empty_description_to_none(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            return None
        return value


class TransactionResponse(BaseModel):
    id: str
    type: TransactionType
    amount: str
    category_id: str
    category_name: str
    date: datetime
    description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(extra="forbid")


class TransactionListResponse(BaseModel):
    items: list[TransactionResponse]
    total: int
    limit: int
    offset: int
