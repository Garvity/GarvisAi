FROM python:3.12-slim

WORKDIR /app

COPY shared ./shared
RUN pip install -e /app/shared

COPY services/auth/requirements.txt ./services/auth/

WORKDIR /app/services/auth
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY services/auth ./services/auth

WORKDIR /app/services/auth

EXPOSE 8001

CMD ["python", "main.py"]