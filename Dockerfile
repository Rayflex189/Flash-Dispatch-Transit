# Use Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=flash_dispatch.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY flash_dispatch/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY flash_dispatch/ .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Run the application with gunicorn
CMD ["gunicorn", "flash_dispatch.wsgi:application", "--bind", "0.0.0.0:8060", "--workers", "4", "--worker-class", "sync"]