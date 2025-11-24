FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system build tools so rpi_ws281x can compile
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    make \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

EXPOSE 5000

CMD ["python", "server.py"]
