import json
import re
import time

from config.agent_limit import check_agent_limit, error_message
from config.llm_models import get_model
from utils.deduct_credits import deduct_credits
from utils.generate_pdf import generate_pdf
from utils.upload_to_s3 import upload_to_s3
from utils.get_from_s3 import get_from_s3



async def pdf_agent(state):
    try:
        await check_agent_limit(state.get("userId"), "pdf")
        llm = await get_model("pdf")
        prompt = f"""
        You are an expert document writer.
Return ONLY valid JSON.
Do NOT return markdown.
Do NOT return explanations.
Structure:
{{
"title":"",
"subtitle":"",
"sections": [
{{
"heading": "",
"points": []
}}
]
}}
Generate 4-8 sections.
Each Section should have 3-6 concise bullet points.
Topic:{state.get("prompt")}
        """
        res = await llm.ainvoke(prompt)
        cleaned = re.sub(r"```json|```", "", res.content).strip()
        data = json.loads(cleaned)
        await deduct_credits(state.get("userId"), "pdf")
        pdf_buffer = await generate_pdf(data)

        file_name = f"pdf-{int(time.time() * 1000)}.pdf"
        upload_to_s3(file_name,pdf_buffer, "application/pdf")
        download_url = get_from_s3(file_name, 10 * 60)
        response = {
            **state,
            "aiResponse": f"""
     📄 PDF Generated Successfully! 🎉

**{data.get("title")}**

📥 **[Download PDF]({download_url})**

⏳ **Note:** This download link expires in **10 minutes**.""",
        }
        print(response)
        return response
    except Exception as err:
        print("Error in pdfAgent:", err)
        return {
            **state,
            "aiResponse": error_message(
                err, " Failed to generate PDF. Please try again later."
            ),
        }
