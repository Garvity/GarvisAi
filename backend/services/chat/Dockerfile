FROM python:3.12-slim

WORKDIR /app

COPY shared ./shared
RUN pip install -e /app/shared

COPY services/chat/requirements.txt ./services/chat/

WORKDIR /app/services/chat
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY services/chat ./services/chat

WORKDIR /app/services/chat

EXPOSE 8002

CMD ["python", "main.py"]