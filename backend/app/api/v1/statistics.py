from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pymongo.asynchronous.database import AsyncDatabase

from app.db.mongo import get_database
from app.modules.statistics.schemas import StatisticsResponse
from app.modules.statistics.service import get_statistics

router = APIRouter(prefix="/statistics", tags=["Statistics"])


@router.get("/summary", response_model=StatisticsResponse)
async def statistics_summary(
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    database: AsyncDatabase = Depends(get_database),
):
    try:
        return await get_statistics(database, date_from, date_to)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
