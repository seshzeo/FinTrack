from pydantic import BaseModel, ConfigDict


class CategoryStatistic(BaseModel):
    category_id: str
    category_name: str
    income: str
    expense: str
    balance: str

    model_config = ConfigDict(extra="forbid")


class StatisticsResponse(BaseModel):
    date_from: str | None
    date_to: str | None
    total_income: str
    total_expense: str
    balance: str
    operations_count: int
    categories: list[CategoryStatistic]

    model_config = ConfigDict(extra="forbid")
