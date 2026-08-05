import os

from motor.motor_asyncio import AsyncIOMotorClient


async def connect_db():
    try:
        client = AsyncIOMotorClient(os.environ["MONGODB_URI"])
        await client.admin.command("ping")
        print("connected to mongo db")
    except Exception as err:
        print("error connecting to mongo db", err)
