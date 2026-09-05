FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.11.19 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_CACHE=1

WORKDIR /app

COPY services/chat ./services/chat

WORKDIR /app/services/chat

RUN uv sync --frozen --no-dev

ENV PATH="/app/services/chat/.venv/bin:$PATH"

EXPOSE 8002

CMD ["python", "main.py"]
