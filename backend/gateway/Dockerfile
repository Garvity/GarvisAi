FROM python:3.12-slim

WORKDIR /app

COPY shared ./shared
RUN pip install -e /app/shared

COPY gateway/requirements.txt ./gateway/

WORKDIR /app/gateway
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY gateway ./gateway

WORKDIR /app/gateway

EXPOSE 8000

CMD ["python", "main.py"]

