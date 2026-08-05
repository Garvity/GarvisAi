import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from controllers.user_controller import get_current_user
from middleware.auth import protect
from utils.proxy import proxy_request

PORT = int(os.environ.get("PORT", 8000))

AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL")
CHAT_SERVICE_URL = os.environ.get("CHAT_SERVICE_URL")
AGENT_SERVICE_URL = os.environ.get("AGENT_SERVICE_URL")
BILLING_SERVICE_URL = os.environ.get("BILLING_SERVICE_URL")

METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("FRONTEND_URL")] if os.environ.get("FRONTEND_URL") else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.api_route("/api/auth/{path:path}", methods=METHODS)
async def auth_proxy(request: Request, path: str = ""):
    return await proxy_request(request, AUTH_SERVICE_URL, path)


@app.api_route("/api/chat/{path:path}", methods=METHODS)
async def chat_proxy(request: Request, path: str = ""):
    user, error = await protect(request)
    if error:
        return error
    return await proxy_request(request, CHAT_SERVICE_URL, path, user)


@app.api_route("/api/agent/{path:path}", methods=METHODS)
async def agent_proxy(request: Request, path: str = ""):
    user, error = await protect(request)
    if error:
        return error
    return await proxy_request(request, AGENT_SERVICE_URL, path, user)


@app.api_route("/api/billing/{path:path}", methods=METHODS)
async def billing_proxy(request: Request, path: str = ""):
    user, error = await protect(request)
    if error:
        return error
    return await proxy_request(request, BILLING_SERVICE_URL, path, user)


@app.get("/api/me")
async def me(request: Request):
    user, error = await protect(request)
    if error:
        return error
    return await get_current_user(user)


@app.get("/")
def root():
    return {"message": "Hello from gateway"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=PORT)
