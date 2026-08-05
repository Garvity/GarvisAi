import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from config.db import connect_db
from routes.chat_route import router

PORT = int(os.environ.get("PORT", 8002))


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.get("/")
def root():
    return {"message": "hello from chat service"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=PORT)
