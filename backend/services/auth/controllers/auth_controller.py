import json
import uuid
from datetime import datetime, timedelta, timezone

from beanie import PydanticObjectId
from fastapi import Request
from fastapi.responses import JSONResponse
from firebase_admin import auth as firebase_auth

from models.user import User, utc_now
from utils.serialize import serialize
from shared.redis_client import redis

SESSION_TTL = 60 * 60 * 24 * 7  # 7 days, same as Node

COST = {
    "chat": 1,
    "search": 5,
    "coding": 10,
    "image": 10,
    "pdf": 10,
    "ppt": 10,
}


def _session_payload(user: User) -> str:
    """Same JSON payload Node stores in session-{id} (undefined fields omitted)."""
    payload = {
        "userId": str(user.id),
        "name": user.name,
        "email": user.email,
        "avatar": user.avatar,
        "plan": user.plan,
        "credits": user.credits,
        "totalCredits": user.totalCredits,
        "planExpiresAt": (
            user.planExpiresAt.strftime("%Y-%m-%dT%H:%M:%S.")
            + f"{user.planExpiresAt.microsecond // 1000:03d}Z"
            if user.planExpiresAt
            else None
        ),
    }
    return json.dumps({k: v for k, v in payload.items() if v is not None})


async def _refresh_session(user: User):
    session_id = await redis.get(f"user-{user.id}")
    await redis.set(f"session-{session_id}", _session_payload(user), ex=SESSION_TTL)


async def login(request: Request):
    try:
        body = await request.json()
        token = body.get("token")
        decoded_token = firebase_auth.verify_id_token(token)
        user = await User.find_one(User.firebaseUid == decoded_token["uid"])
        if user is None:
            user = User(
                firebaseUid=decoded_token["uid"],
                name=decoded_token.get("name"),
                email=decoded_token.get("email"),
                avatar=decoded_token.get("picture"),
            )
            await user.insert()
        session_id = str(uuid.uuid4())
        await redis.set(f"user-{user.id}", session_id, ex=SESSION_TTL)
        await redis.set(f"session-{session_id}", _session_payload(user), ex=SESSION_TTL)
        response = JSONResponse(status_code=200, content=serialize(user))
        response.set_cookie(
            "session",
            session_id,
            httponly=True,
            secure=False,
            samesite="strict",
            max_age=60 * 60 * 24 * 7,
        )
        return response
    except Exception as err:
        return JSONResponse(status_code=500, content={"message": f"login error: {err}"})


async def log_out(request: Request):
    try:
        session_id = request.cookies.get("session")
        await redis.delete(f"session-{session_id}")
        response = JSONResponse(
            status_code=200, content={"message": "logout successful"}
        )
        response.delete_cookie("session")
        return response
    except Exception as err:
        return JSONResponse(
            status_code=500, content={"message": f"logout error: {err}"}
        )


async def update_user_payment_status(request: Request):
    try:
        body = await request.json()
        plan = body.get("plan")
        credits = body.get("credits")
        user_id = body.get("userId")
        user = await User.get(PydanticObjectId(user_id))
        if user is None:
            return JSONResponse(status_code=404, content={"message": "User not found"})
        user.plan = plan
        user.credits += credits
        user.totalCredits += credits
        user.planExpiresAt = datetime.now(timezone.utc) + timedelta(days=30)
        user.updatedAt = utc_now()
        await user.save()
        await _refresh_session(user)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "User payment status updated successfully",
            },
        )
    except Exception as err:
        return JSONResponse(
            status_code=500,
            content={"message": f"updateUserPaymentStatus error: {err}"},
        )


async def deduct_credits(request: Request):
    try:
        body = await request.json()
        agent = body.get("agent")
        user_id = body.get("userId")
        user = await User.get(PydanticObjectId(user_id))
        if user is None:
            return JSONResponse(status_code=404, content={"message": "User not found"})
        required_credits = COST.get(agent) or 1
        if user.credits < required_credits:
            return JSONResponse(
                status_code=400, content={"message": "Insufficient credits"}
            )
        user.credits -= required_credits
        user.updatedAt = utc_now()
        await user.save()
        await _refresh_session(user)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Credits deducted successfully",
                "credits": user.credits,
            },
        )
    except Exception as err:
        return JSONResponse(
            status_code=500, content={"message": f"deductCredits error: {err}"}
        )
