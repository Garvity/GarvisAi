import json
import time

from config.agent_limit import check_agent_limit, error_message
from config.llm_models import get_model
from utils.deduct_credits import deduct_credits


async def coding_agent(state):
    try:
        await check_agent_limit(state.get("userId"), "coding")
        intent_llm = await get_model("intent")
        llm = await get_model("coding")
        intent_res = await intent_llm.ainvoke(f"""
        You are an intent classifier.
        Return ONLY one of these values.
        CODE_GENERATION
        CODE_REVIEW
        CODE_EXPLANATION
        DEBUGGING
        OPTIMIZATION
        CONVERSION
        DOCUMENTATION
        User Request:{state.get("prompt")}
    """)
        intent = intent_res.content
        if intent == "CODE_GENERATION":
            prompt = f"""
        You are GarvisAI Coding Agent.
Generate the requested project.

Default stack:
- HTML
- CSS
- JavaScript

Use React / Next.js / Vue ONLY if explicitly requested.

Rules:
- Responsive
- Modern UI
- CSS Variables
- Flexbox/Grid
- Smooth Scroll
- Hover Effects
- Beautiful spacing
- Single page unless user asks otherwise.

IMAGES
=========================
Always use real unsplash images.
Never use placeholder.

Return ONLY valid JSON.

Schema:
{{
    "files":[
    {{
        "name":"index.html",
        "content":"..."
    }},
    {{
        "name":"style.css",
        "content":"..."
    }},
    {{
        "name":"script.js",
        "content":"..."
    }}
    ]
}}

Rules:

- Output must start with {{
- Output must end with }}
- No markdown
- No explanation
- No extra text
- No ```
- Never mention intent

User Request:{state.get("prompt")}
        """
            res = await llm.ainvoke(prompt)
            data = json.loads(res.content)
            await deduct_credits(state.get("userId"), "coding")
            print("coding agent res", data)
            return {
                **state,
                "aiResponse": "Code Generated Successfully",
                "artifacts": [
                    {
                        "id": int(time.time() * 1000),
                        "type": "project",
                        "files": data.get("files") or [],
                        "title": state.get("prompt"),
                    }
                ],
            }
        res = await llm.ainvoke(f"""
        The user's request is:
{intent}
Return Markdown only.
Never generate project files.
Use headings like:
# Overview
## Explanation
## Problems
## Improvements
## Best Practices
## Optimized Code (if needed)
User Request:{state.get("prompt")}
        """)
        data = res.content
        return {**state, "aiResponse": data, "artifacts": []}
    except Exception as err:
        print("Error in codingAgent:", err)
        return {
            **state,
            "aiResponse": error_message(
                err, "Failed to process coding request. Please try again later."
            ),
            "artifacts": [],
        }
