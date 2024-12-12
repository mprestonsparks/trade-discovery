FROM python:3.10-slim

WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY pyproject.toml .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .

# Copy the rest of the application
COPY . .

EXPOSE 8084

# Use the new module path
CMD ["uvicorn", "trade_discovery.main:app", "--host", "0.0.0.0", "--port", "8084", "--reload"]
