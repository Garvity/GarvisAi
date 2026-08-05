from beanie import PydanticObjectId
from fastapi import Request
from fastapi.responses import JSONResponse

from models.conversation import Conversation, utc_now
from models.message import Message
from utils.serialize import serialize


async def create_conversation(request: Request):
    try:
        user_id = request.headers.get("x-user-id")
        print("userId", user_id)
        conversation = Conversation(userId=user_id)
        await conversation.insert()
        return JSONResponse(status_code=200, content=serialize(conversation))
    except Exception as err:
        return JSONResponse(
            status_code=500, content={"message": f"createConversation error: {err}"}
        )


async def get_conversations(request: Request):
    try:
        user_id = request.headers.get("x-user-id")
        print("userId", user_id)
        conversations = (
            await Conversation.find(Conversation.userId == user_id)
            .sort("-updatedAt")
            .to_list()
        )
        return JSONResponse(
            status_code=200, content=[serialize(c) for c in conversations]
        )
    except Exception as err:
        return JSONResponse(
            status_code=500, content={"message": f"getConversations error: {err}"}
        )


async def save_message(request: Request):
    try:
        body = await request.json()
        message = Message(
            conversationId=body.get("conversationId"),
            role=body.get("role"),
            content=body.get("content"),
            images=body.get("images") or [],
            artifacts=body.get("artifacts") or [],
        )
        await message.insert()
        return JSONResponse(status_code=200, content=serialize(message))
    except Exception as err:
        return JSONResponse(
            status_code=500, content={"message": f"saveMessage error: {err}"}
        )


async def get_messages(conversation_id: str):
    try:
        messages = await Message.find(
            Message.conversationId == PydanticObjectId(conversation_id)
        ).to_list()
        return JSONResponse(status_code=200, content=[serialize(m) for m in messages])
    except Exception as err:
        return JSONResponse(
            status_code=500, content={"message": f"getMessages error: {err}"}
        )


async def update_conversation(request: Request):
    try:
        body = await request.json()
        conversation = await Conversation.get(PydanticObjectId(body.get("id")))
        if conversation is not None:
            conversation.title = body.get("title")
            conversation.updatedAt = utc_now()
            await conversation.save()
        return JSONResponse(status_code=200, content=serialize(conversation))
    except Exception as err:
        return JSONResponse(
            status_code=500,
            content={"message": f"updateConversationTitle error: {err}"},
        )
