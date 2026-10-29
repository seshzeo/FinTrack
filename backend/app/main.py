
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pymongo.errors import PyMongoError

from app.core.config import get_settings
from app.db.mongo import (
    close_mongo_connection,
    connect_to_mongo,
    get_database,
)

from app.api.v1.categories import router as categories_router
from app.api.v1.transactions import router as transactions_router
from app.api.v1.statistics import router as statistics_router


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    try:
        from app.db.indexes import create_indexes
        from app.db.seed import seed_categories
        
        database = get_database()
        
        await create_indexes(database)
        await seed_categories(database)
        
        yield
    finally:
        await close_mongo_connection()


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)


app.include_router(categories_router, prefix=settings.api_v1_prefix)
app.include_router(transactions_router, prefix=settings.api_v1_prefix)
app.include_router(statistics_router, prefix=settings.api_v1_prefix)


@app.get("/health")
async def health():
    try:
        await get_database().command("ping")
        return {"status": "ok", "database": "connected"}
    except (RuntimeError, PyMongoError):
        raise HTTPException(
            status_code=503,
            detail={
                "code": "DATABASE_UNAVAILABLE",
                "message": "Database is unavailable",
            },
        )


@app.get(f"{settings.api_v1_prefix}/health")
async def api_health():
    return await health()
