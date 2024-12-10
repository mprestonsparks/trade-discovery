FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8084

CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8084", "--reload"]
