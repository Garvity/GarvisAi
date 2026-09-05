FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.11.19 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_CACHE=1

WORKDIR /app

COPY shared ./shared
COPY gateway ./gateway

WORKDIR /app/gateway

RUN uv sync --frozen --no-dev

ENV PATH="/app/gateway/.venv/bin:$PATH"

EXPOSE 8000

CMD ["python", "main.py"]
