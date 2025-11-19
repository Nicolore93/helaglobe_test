
FROM python:3.11-bullseye

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Set working dir inside container
WORKDIR /app
COPY . .

# Imposta PYTHONPATH per sicurezza
ENV PYTHONPATH=/app

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--root-path", "/api"]

