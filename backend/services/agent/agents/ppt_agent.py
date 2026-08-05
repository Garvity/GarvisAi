import json
import re
import time

from config.agent_limit import check_agent_limit, error_message
from config.llm_models import get_model
from utils.deduct_credits import deduct_credits
from utils.generate_ppt import generate_ppt
from utils.upload_to_s3 import upload_to_s3
from utils.get_from_s3 import get_from_s3



async def ppt_agent(state):
    try:
        await check_agent_limit(state.get("userId"), "ppt")
        llm = await get_model("ppt")
        prompt = f"""You are a professional presentation designer.
Return ONLY valid JSON.
Format:
{{
"title":"",
"subtitle":"",
"slides": [
{{
"title":"",
"points": [
"",
"",
"",
""
]

Rules:
-Generate exactly 6 content slides.
- Each slide should have a clear and concise title.
- Each slide should have 4-6  concise bullet points.
- No markdown.
- No explanation.
- No code block.
- Return only valid JSON.

Topic:{state.get("prompt")}
"""
        res = await llm.ainvoke(prompt)
        cleaned = re.sub(r"```json|```", "", res.content).strip()
        data = json.loads(cleaned)
        await deduct_credits(state.get("userId"), "ppt")
        buffer = await generate_ppt(data)
        file_name = f"ppt-{int(time.time() * 1000)}.pptx"
        upload_to_s3(
            file_name,
            buffer,
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        )
        download_url = get_from_s3(file_name, 24 * 60 * 60)
        
        return {
            **state,
            "aiResponse": f"""
     📊 PPT Generated Successfully! 🎉

**{data.get("title")}**
📥 **[Download PPT]({download_url})**
⏳ **Note:** This download link expires in **10 minutes**.""",
        }
    except Exception as err:
        print("Error in pptAgent:", err)
        return {
            **state,
            "aiResponse": error_message(
                err, " Failed to generate PPT. Please try again later."
            ),
        }
