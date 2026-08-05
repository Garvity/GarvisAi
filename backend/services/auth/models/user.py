from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


def utc_now():
    return datetime.now(timezone.utc)


class User(Document):
    firebaseUid: str | None = None
    name: str | None = None
    email: str | None = None
    avatar: str | None = None
    plan: str = "free"
    credits: int = 100
    totalCredits: int = 100
    planExpiresAt: datetime | None = None
    createdAt: datetime = Field(default_factory=utc_now)
    updatedAt: datetime = Field(default_factory=utc_now)
    version: int = Field(default=0, alias="__v")

    class Settings:
        name = "users"
