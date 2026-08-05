import os

import httpx


async def get_messages(conversation_id):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{os.environ.get('CHAT_SERVICE_URL')}/get-messages/{conversation_id}"
            )
            return resp.json()
    except Exception as error:
        print("Error fetching messages:", error)
        return None
