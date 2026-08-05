from datetime import datetime, timezone
from typing import Literal

from beanie import Document
from pydantic import Field


def utc_now():
    return datetime.now(timezone.utc)


class Payment(Document):
    userId: str
    orderId: str
    paymentId: str | None = None
    amount: float | None = None
    currency: str = "INR"
    credits: int | None = None
    plan: str | None = None
    status: Literal["created", "paid", "failed"] = "created"
    createdAt: datetime = Field(default_factory=utc_now)
    updatedAt: datetime = Field(default_factory=utc_now)
    version: int = Field(default=0, alias="__v")

    class Settings:
        name = "payments"
