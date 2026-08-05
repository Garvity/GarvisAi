from fastapi import APIRouter

from controllers.agent_controller import agent

router = APIRouter()

router.add_api_route("/chat", agent, methods=["POST"])
