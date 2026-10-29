from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.config import get_settings


settings = get_settings()

client: AsyncMongoClient | None = None
database: AsyncDatabase | None = None


async def connect_to_mongo() -> None:
    global client, database

    mongo_client = AsyncMongoClient(
        settings.mongodb_uri,
        serverSelectionTimeoutMS=3000,
    )

    try:
        await mongo_client.admin.command("ping")
    except Exception:
        await mongo_client.close()
        raise

    client = mongo_client
    database = client[settings.mongodb_database]


async def close_mongo_connection() -> None:
    global client, database

    if client is not None:
        await client.close()

    client = None
    database = None


def get_database() -> AsyncDatabase:
    if database is None:
        raise RuntimeError("MongoDB connection is not initialized")

    return database