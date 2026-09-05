FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.11.19 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_CACHE=1

WORKDIR /app

COPY shared ./shared
COPY services/auth ./services/auth

WORKDIR /app/services/auth

RUN uv sync --frozen --no-dev

ENV PATH="/app/services/auth/.venv/bin:$PATH"

EXPOSE 8001

CMD ["python", "main.py"]
