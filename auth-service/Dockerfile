FROM python:3.12-slim

WORKDIR /app

# Sistema: librerías necesarias para compilar psycopg2
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Code
COPY test_connection.py /app/test_connection.py

# Default command (override en docker-compose)
CMD ["python", "/app/test_connection.py"]
