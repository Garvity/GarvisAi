from shared.redis_client import redis

LIMITS = {
    "chat": 20,
    "coding": 5,
    "pdf": 5,
    "ppt": 5,
    "image": 5,
    "search": 5,
}


class AgentLimitError(Exception):
    """Mirror of the Node error object with status and data attached."""

    def __init__(self, message, status, data):
        super().__init__(message)
        self.status = status
        self.data = data


def error_message(err, fallback):
    """Mirror of Node's `err?.data?.message || fallback`."""
    data = getattr(err, "data", None)
    if isinstance(data, dict) and data.get("message"):
        return data["message"]
    return fallback


async def check_agent_limit(user_id, agent):
    max_limit = LIMITS.get(agent) or LIMITS["chat"]
    key = f"rate:{agent}-{user_id}"
    count = await redis.incr(key)
    if count == 1:
        await redis.expire(key, 60)
    ttl = await redis.ttl(key)
    if count > max_limit:
        minutes = ttl // 60
        seconds = ttl % 60
        time_str = (
            f"{minutes} minute(s) and {seconds} second(s)"
            if minutes > 0
            else f"{seconds} second(s)"
        )
        raise AgentLimitError(
            f"You have exceeded the limit for {agent} agent. Please wait for {time_str} before trying again.",
            status=429,
            data={
                "success": False,
                "limit": max_limit,
                "agent": agent,
                "remainingTime": ttl,
                "retryTime": time_str,
                "message": f"You have exceeded the limit ({max_limit} requests/minute) for {agent} agent . Please wait for {time_str} before trying again.",
            },
        )
    return {"remaining": max_limit - count, "limit": max_limit}
