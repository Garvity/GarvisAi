import json

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from config.agent_limit import check_agent_limit, error_message
from config.llm_models import get_model
from config.memory import get_memory
from utils.deduct_credits import deduct_credits


async def chat_agent(state):
    try:
        await check_agent_limit(state.get("userId"), "chat")
        llm = await get_model("chat")

        history = await get_memory(state.get("conversationId"))

        search_context = (
            f"""Web Search Results
    {json.dumps(state.get("searchResults"))}
    Answer the user using the above search results and your own knowledge"""
            if state.get("searchResults")
            else ""
        )

        system_prompt = f"""You are GarvisAI, an intelligent AI assistant.

        {search_context}
    if searchContext exists:
    - Use the search results to answer the user's question.
    - Do not mention internal tools

    Rules:
- For simple questions, greetings, and short queries, respond naturally in plain text.
- For technical, educational, coding, or detailed topics, use clean Markdown.
    Formatting:
- Use # for titles and ## for sections.
- Leave a blank line after headings.
- Use bullet points for lists.
- Use numbered lists for steps.
- Use fenced code blocks with language tags for code.
- Keep paragraphs short and readable.
- Never write headings and content on the same line.
- Never generate large walls of text.
    """
        messages = [SystemMessage(system_prompt)]

        for message in history or []:
            if message.get("role") == "user":
                messages.append(HumanMessage(message.get("content")))
            if message.get("role") == "assistant":
                messages.append(AIMessage(message.get("content")))

        messages.append(HumanMessage(state.get("prompt")))
        print(messages)

        response = await llm.ainvoke(messages)
        await deduct_credits(state.get("userId"), "chat")
        return {**state, "aiResponse": response.content}
    except Exception as err:
        print("Error in chatAgent:", err)
        return {
            **state,
            "aiResponse": error_message(
                err, "Failed to generate response. Please try again later."
            ),
        }
