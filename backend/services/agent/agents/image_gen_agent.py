import time
import urllib.parse

import httpx

from config.agent_limit import check_agent_limit, error_message
from config.llm_models import get_model
from utils.deduct_credits import deduct_credits
from utils.upload_to_s3 import upload_to_s3
from utils.get_from_s3 import get_from_s3


async def image_gen_agent(state):
    try:
        await check_agent_limit(state.get("userId"), "image")
        llm = await get_model("image")
        res = await llm.ainvoke(f"""You are an elite AI image prompt engineer.
Convert the user request into a highly detailed image generation prompt.
Requirements:

- Cinematic lighting
- Professional composition
- Ultra realistic
- High detail
- Beautiful color palette
- Sharp focus
- 8K quality
- Photorealistic
- Depth of field
- Professional photography
- Stunning visuals

Return only the image prompt.
User Request:{state.get("prompt")}
""")
        prompt = res.content.strip()
        image_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt, safe='')}"
        async with httpx.AsyncClient(timeout=None) as client:
            image_res = await client.get(image_url)
        await deduct_credits(state.get("userId"), "image")
        image_buffer = image_res.content
        file_name = f"image_{int(time.time() * 1000)}.png"
        upload_to_s3(file_name, image_buffer, "image/png")
        download_url = get_from_s3(file_name, 24 * 60 * 60)
        return {
            **state,
            "aiResponse": f"""
     🖼️ Image Generated Successfully! 🎉

![Generated Image]({download_url})

📥 **[Download Image]({download_url})**

⏳ **Note:** This download link expires in **10 minutes**.""",
        }
    except Exception as err:
        print("Error in imageGenAgent:", err)
        return {
            **state,
            "aiResponse": error_message(
                err, "Failed to generate image. Please try again later."
            ),
        }
