from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


def utc_now():
    return datetime.now(timezone.utc)


class Conversation(Document):
    title: str = "New Chat"
    userId: str | None = None
    createdAt: datetime = Field(default_factory=utc_now)
    updatedAt: datetime = Field(default_factory=utc_now)
    version: int = Field(default=0, alias="__v")

    class Settings:
        name = "conversations"
