# Use Python 3.11 (more stable with crispy-tailwind)
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=flash_dispatch.settings

# Set work directory
WORKDIR /code

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

# Copy entrypoint script from repository root
COPY entrypoint.sh /code/entrypoint.sh

# Create necessary directories
RUN mkdir -p static media staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /code

# Make entrypoint executable
RUN chmod +x /code/entrypoint.sh

USER appuser

# Start application
ENTRYPOINT ["/code/entrypoint.sh"]
