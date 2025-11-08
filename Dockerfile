FROM python:3.12-slim

WORKDIR /app
# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=trendvault.settings

# Install system dependencies for PostgreSQL
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy project code
COPY static trendvault youtube .

# Copy dependency files
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync

RUN uv run python manage.py migrate

