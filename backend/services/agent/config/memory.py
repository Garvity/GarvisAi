import json

from shared.redis_client import redis

from utils.get_messages import get_messages


async def get_memory(conversation_id):
    key = f"messages:{conversation_id}"
    cached = await redis.get(key)
    if cached:
        return json.loads(cached)
    messages = await get_messages(conversation_id)
    await redis.set(key, json.dumps(messages), ex=60 * 60 * 24)
    return messages


async def add_message(conversation_id, role, content):
    key = f"messages:{conversation_id}"
    cached = await redis.get(key)
    messages = []
    if cached:
        messages = json.loads(cached)
    messages.append({"role": role, "content": content})
    if len(messages) > 20:
        messages.pop(0)
    await redis.set(key, json.dumps(messages))
