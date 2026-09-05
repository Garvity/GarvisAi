# Build from the backend root:
# docker build -f services/agent/Dockerfile .

FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.11.19 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_CACHE=1

WORKDIR /app

COPY shared ./shared
COPY services/agent ./services/agent

WORKDIR /app/services/agent

RUN uv sync --frozen --no-dev

ENV PATH="/app/services/agent/.venv/bin:$PATH"

EXPOSE 8003

CMD ["python", "main.py"]
