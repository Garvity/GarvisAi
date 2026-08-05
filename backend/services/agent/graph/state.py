from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    prompt: str
    aiResponse: str
    agent: str
    conversationId: str
    searchResults: Any
    images: Any
    artifacts: Any
    userId: str
    file: Any
