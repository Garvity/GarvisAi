import httpx
from fastapi import Request, Response

# No timeout: LLM-backed agent requests can run long (Node has no proxy timeout).
client = httpx.AsyncClient(timeout=None)

# Headers that must not be forwarded verbatim. content-encoding/content-length
# are dropped from responses because httpx transparently decompresses bodies.
EXCLUDED_REQUEST_HEADERS = {"host", "content-length"}
EXCLUDED_RESPONSE_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
    "content-encoding",
    "content-length",
}


async def proxy_request(
    request: Request, service_url: str, path: str, user: dict | None = None
) -> Response:
    """Forward a request to a service, mirroring express-http-proxy.

    The mount prefix is already stripped (path is the remainder). When a
    user is present and has userId, inject x-user-id like proxyWithHeader.
    """
    url = service_url.rstrip("/") + "/" + path
    if request.url.query:
        url += "?" + request.url.query

    headers = {
        k: v
        for k, v in request.headers.items()
        if k.lower() not in EXCLUDED_REQUEST_HEADERS
    }
    if user and user.get("userId"):
        headers["x-user-id"] = user["userId"]

    body = await request.body()
    resp = await client.request(request.method, url, headers=headers, content=body)

    response_headers = {
        k: v
        for k, v in resp.headers.items()
        if k.lower() not in EXCLUDED_RESPONSE_HEADERS
    }
    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=response_headers,
        media_type=resp.headers.get("content-type"),
    )
