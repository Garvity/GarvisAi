from config.agent_limit import check_agent_limit, error_message
from config.tavily import search_tool
from utils.deduct_credits import deduct_credits


async def search_agent(state):
    try:
        await check_agent_limit(state.get("userId"), "search")
        results = await search_tool.ainvoke({"query": state.get("prompt")})
        await deduct_credits(state.get("userId"), "search")
        print("Search results:", results)
        images = results.get("images") if isinstance(results, dict) else None
        return {**state, "searchResults": results, "images": images}
    except Exception as err:
        print("Error occurred while searching:", err)
        return {
            **state,
            "searchResults": [],
            "images": [],
            "aiResponse": error_message(
                err, "Failed to perform search. Please try again later."
            ),
        }
