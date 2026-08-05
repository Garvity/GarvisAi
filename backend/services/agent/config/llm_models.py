import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

load_dotenv()

groq = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.environ.get("GROQ_API_KEY"),
)

gemini = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GOOGLE_API_KEY"),
)

# No OpenRouter partner package exists for Python; ChatOpenAI with the
# OpenRouter base URL is the documented equivalent of @langchain/openrouter.
openrouter = ChatOpenAI(
    model="deepseek/deepseek-chat",
    temperature=0,
    max_tokens=2500,
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)


async def get_model(agent):
    match agent:
        case "chat":
            return groq
        case "search":
            return groq
        case "coding":
            return openrouter
        case "pdf":
            return groq
        case "ppt":
            return groq
        case "image":
            return gemini
        case "pdfRag":
            return groq
        case "imageAnalyzer":
            return gemini
        case _:
            return groq
