FROM python:3.12-slim

WORKDIR /app

COPY shared ./shared
RUN pip install -e /app/shared

COPY services/billing/requirements.txt ./services/billing/

WORKDIR /app/services/billing
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY services/billing ./services/billing

WORKDIR /app/services/billing

EXPOSE 8004

CMD ["python", "main.py"]