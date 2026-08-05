from datetime import datetime

from beanie import Document, PydanticObjectId
from pydantic import BaseModel


def _convert(value):
    if isinstance(value, datetime):
        # mongoose JSON format: 2026-07-20T13:48:43.320Z
        return value.strftime("%Y-%m-%dT%H:%M:%S.") + f"{value.microsecond // 1000:03d}Z"
    if isinstance(value, PydanticObjectId):
        return str(value)
    if isinstance(value, dict):
        return {k: _convert(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_convert(v) for v in value]
    return value


def serialize(doc: Document | BaseModel | None):
    """Serialize a Beanie document to the same JSON shape mongoose produces."""
    if doc is None:
        return None
    data = doc.model_dump(by_alias=True, exclude_none=False)
    return _convert(data)
