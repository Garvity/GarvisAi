import os

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models.user import User


async def connect_db():
    try:
        client = AsyncIOMotorClient(os.environ["MONGODB_URI"])
        await init_beanie(
            database=client.get_default_database("test"),
            document_models=[User],
        )
        print("connected to mongo db")
    except Exception as err:
        print("error connecting to mongo db", err)
