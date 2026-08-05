from datetime import datetime, timezone
from typing import Literal

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field


def utc_now():
    return datetime.now(timezone.utc)


class File(BaseModel):
    name: str | None = None
    content: str | None = None


class Artifact(BaseModel):
    id: int | None = None
    type: str | None = None
    title: str | None = None
    files: list[File] = []


class Message(Document):
    conversationId: PydanticObjectId | None = None
    role: Literal["user", "assistant"] | None = None
    content: str | None = None
    images: list[str] = []
    artifacts: list[Artifact] = []
    createdAt: datetime = Field(default_factory=utc_now)
    updatedAt: datetime = Field(default_factory=utc_now)
    version: int = Field(default=0, alias="__v")

    class Settings:
        name = "messages"
