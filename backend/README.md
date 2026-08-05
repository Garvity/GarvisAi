# Cortex AI — Python backend (FastAPI)

FastAPI port of the Node/Express microservices in `../backend`. The frontend is
unchanged: all routes, JSON shapes, cookies, and headers match the Node backend.

| Piece | Port | Path |
|---|---|---|
| Gateway | 8000 | `gateway/` |
| Auth | 8001 | `services/auth/` |
| Chat | 8002 | `services/chat/` |
| Agent | 8003 | `services/agent/` |
| Billing | 8004 | `services/billing/` |
| Shared redis client | — | `shared/` |

## Setup

Each service is a [uv](https://docs.astral.sh/uv/) project. Copy the `.env`
from the corresponding Node service into each Python service directory
(same variable names, unchanged), plus `serviceAccountKey.json` into
`services/auth/`. Then:

```sh
docker compose up -d          # redis
cd services/chat && uv sync   # repeat per service (and gateway/)
```

## Run (dev)

From each service directory:

```sh
uv run uvicorn main:app --reload --port <port>   # or: uv run python main.py
```

## Docker

Build from this directory (context must include `shared/`):

```sh
docker build -f gateway/Dockerfile .
docker build -f services/auth/Dockerfile .
# ... same for chat, agent, billing
```
