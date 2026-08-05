# Build from the backend-python root:
# docker build -f services/agent/Dockerfile .

FROM python:3.12-slim

WORKDIR /app

COPY shared ./shared
RUN pip install -e /app/shared

COPY services/agent/requirements.txt ./services/agent/

WORKDIR /app/services/agent
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY services/agent ./services/agent

WORKDIR /app/services/agent

EXPOSE 8003

CMD ["python", "main.py"]