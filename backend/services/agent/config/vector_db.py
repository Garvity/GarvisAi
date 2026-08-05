import asyncio
import os

from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore

from config.embeddings import embeddings

load_dotenv()


async def vector_store(docs, collection_name):
    # Unlike @langchain/qdrant in Node (which reads QDRANT_API_KEY from the
    # environment automatically), langchain-qdrant requires the key explicitly.
    return await asyncio.to_thread(
        QdrantVectorStore.from_documents,
        docs,
        embeddings,
        url=os.environ.get("QDRANT_URL"),
        api_key=os.environ.get("QDRANT_API_KEY"),
        collection_name=collection_name,
    )
