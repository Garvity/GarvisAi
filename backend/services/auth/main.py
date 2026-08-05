import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

import config.firebase  # noqa: F401  (initializes firebase-admin at import, like Node)
from config.db import connect_db
from routes.auth_route import router

PORT = int(os.environ.get("PORT", 8001))


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.get("/")
def root():
    return {"message": "Hello from auth service"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=PORT)
