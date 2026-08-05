import os

import httpx
from fastapi import Request
from fastapi.responses import JSONResponse

from config.memory import add_message
from config.upload import save_upload
from graph.graph import graph


async def agent(request: Request):
    try:
        user_id = request.headers.get("x-user-id")
        file = None
        content_type = request.headers.get("content-type", "")
        if content_type.startswith("multipart/form-data"):
            form = await request.form()
            body = {k: v for k, v in form.items() if isinstance(v, str)}
            upload = form.get("file")
            if upload is not None and not isinstance(upload, str):
                file = await save_upload(upload)
        else:
            body = await request.json()
        print("file", file)
        prompt = body.get("prompt")
        conversation_id = body.get("conversationId")
        agent_name = body.get("agent")
        print("incoming agent:", agent_name, "file present:", bool(file))
        result = await graph.ainvoke(
            {
                "conversationId": conversation_id,
                "prompt": prompt,
                "agent": agent_name,
                "userId": user_id,
                "file": file,
            }
        )
        chat_service_url = os.environ.get("CHAT_SERVICE_URL")
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{chat_service_url}/save-message",
                json={
                    "conversationId": conversation_id,
                    "role": "user",
                    "content": prompt,
                },
            )
            await add_message(conversation_id, "user", prompt)
            await add_message(conversation_id, "assistant", result.get("aiResponse"))
            await client.post(
                f"{chat_service_url}/save-message",
                json={
                    "conversationId": conversation_id,
                    "role": "assistant",
                    "content": result.get("aiResponse"),
                    "images": result.get("images"),
                    "artifacts": result.get("artifacts"),
                },
            )
        return JSONResponse(
            status_code=200,
            content={
                "answer": result.get("aiResponse"),
                "images": result.get("images"),
                "artifacts": result.get("artifacts"),
            },
        )
    except Exception as err:
        # Mirror of the Node error middleware in index.js
        print(err)
        status = getattr(err, "status", None)
        if status:
            return JSONResponse(
                status_code=status,
                content={"error": getattr(err, "data", None) or str(err)},
            )
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})
