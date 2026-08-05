import json

from fastapi import Request
from fastapi.responses import JSONResponse

from shared.redis_client import redis


async def protect(request: Request):
    """Mirror of gateway/middleware/auth.middleware.js.

    Returns (user, None) on success or (None, error_response) — same
    status codes and bodies as Node (400, not 401, by design).
    """
    try:
        session_id = request.cookies.get("session")
        if not session_id:
            return None, JSONResponse(
                status_code=400, content={"message": "Unauthorized"}
            )
        session = await redis.get(f"session-{session_id}")
        if not session:
            return None, JSONResponse(
                status_code=400, content={"message": "session expired"}
            )
        return json.loads(session), None
    except Exception as error:
        return None, JSONResponse(
            status_code=500, content={"message": f"protect error: {error}"}
        )
