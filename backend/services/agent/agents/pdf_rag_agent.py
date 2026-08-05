import asyncio
import os
import time

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from config.agent_limit import check_agent_limit, error_message
from config.llm_models import get_model
from config.vector_db import vector_store
from utils.deduct_credits import deduct_credits


def _extract_text(path):
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


async def pdf_rag_agent(state):
    file = state.get("file")
    try:
        await check_agent_limit(state.get("userId"), "pdfRag")
        text = await asyncio.to_thread(_extract_text, file["path"])
        if not text.strip():
            return {
                **state,
                "aiResponse": (
                    "The uploaded PDF doesn't contain extractable text. "
                    "It may be a scanned document or image-based PDF."
                ),
            }
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = splitter.create_documents([text])
        collection_name = f"pdf-{int(time.time() * 1000)}"
        store = await vector_store(docs, collection_name)
        relevant_docs = await asyncio.to_thread(
            store.similarity_search, query=state.get("prompt"), k=5
        )
        if not relevant_docs:
            return {
                **state,
                "aiResponse": "I couldn't find any relevant information in the uploaded PDF."
            }
        context = "\n\n".join(doc.page_content for doc in relevant_docs)
        llm = await get_model("pdfRag")
        messages = [
            SystemMessage("""You are GarvisAI PDF Assistant.

The user has uploaded a PDF.

Instructions:
- Use only the information contained in the uploaded PDF.
- If the user asks to summarize, analyze, explain, review, or extract information from the document, perform that task using the PDF content.
- If the user asks a specific question, answer it using only the PDF.
- If the answer cannot be found in the PDF, reply:
  "I couldn't find this information in the uploaded PDF."
- Do not invent facts or use outside knowledge.
- Format responses using Markdown."""),
            HumanMessage(
    f"""
Below is the extracted content from the uploaded PDF.

<document>
{context}
</document>

User request:
{state.get("prompt")}
"""
        ),
        ]
        response = await llm.ainvoke(messages)
        await deduct_credits(state.get("userId"), "pdfRag")
        return {**state, "aiResponse": response.content}
    except Exception as err:
        print("Error in pdfRagAgent:", err)
        return {
            **state,
            "aiResponse": error_message(
                err, "Failed to process the PDF. Please try again later."
            ),
        }
    finally:
        if file and file.get("path"):
            os.unlink(file["path"])
