from fastapi import APIRouter

from controllers.chat_controller import (
    create_conversation,
    get_conversations,
    get_messages,
    save_message,
    update_conversation,
)

router = APIRouter()

router.add_api_route("/create-conversation", create_conversation, methods=["GET"])
router.add_api_route("/get-conversations", get_conversations, methods=["GET"])
router.add_api_route("/update-conversation", update_conversation, methods=["POST"])
router.add_api_route("/save-message", save_message, methods=["POST"])
router.add_api_route("/get-messages/{conversation_id}", get_messages, methods=["GET"])
