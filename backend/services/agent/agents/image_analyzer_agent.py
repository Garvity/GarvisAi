import base64
import os

from langchain_core.messages import HumanMessage, SystemMessage

from config.agent_limit import check_agent_limit, error_message
from config.llm_models import get_model
from utils.deduct_credits import deduct_credits


async def image_analyzer_agent(state):
    try:
        await check_agent_limit(state.get("userId"), "imageAnalyzer")
        llm = await get_model("imageAnalyzer")
        file = state.get("file")
        with open(file["path"], "rb") as f:
            image_buffer = f.read()
        base64_image = base64.b64encode(image_buffer).decode()
        messages = [
            SystemMessage("""You are GarvisAI image analyzer Agent.
Rules:
- Analyze only the uploaded image.
- Answer the user's question accurately.
- If text exists in the image, extract it.
- If charts or tables exist, explain them.
- If something is unclear, say so.
- Use Markdown when helpful.
- Do not hallucinate."""),
            HumanMessage(
                content=[
                    {
                        "type": "text",
                        "text": state.get("prompt")
                        or "Analyze the uploaded image and provide insights.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{file['mimetype']};base64,{base64_image}"
                        },
                    },
                ]
            ),
        ]
        response = await llm.ainvoke(messages)
        await deduct_credits(state.get("userId"), "imageAnalyzer")
        return {**state, "aiResponse": response.content}
    except Exception as err:
        print("Error in imageAnalyzerAgent:", err)
        return {
            **state,
            "aiResponse": error_message(
                err, "Failed to analyze the image. Please try again later."
            ),
        }
    finally:
        file = state.get("file")
        if file and file.get("path"):
            try:
                os.unlink(file["path"])
            except Exception as err:
                print("Failed to delete temporary file:", err)
