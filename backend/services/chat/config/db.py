import os

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models.conversation import Conversation
from models.message import Message


async def connect_db():
    try:
        client = AsyncIOMotorClient(os.environ["MONGODB_URI"])
        await init_beanie(
            database=client.get_default_database("test"),
            document_models=[Conversation, Message],
        )
        print("connected to mongo db")
    except Exception as err:
        print("error connecting to mongo db", err)
