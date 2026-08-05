import os

import httpx


async def deduct_credits(user_id, agent):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{os.environ.get('AUTH_SERVICE_URL')}/deduct-credits",
                json={"userId": user_id, "agent": agent},
            )
            return resp.json()
    except Exception as error:
        print("Error fetching messages:", error)
        return None
