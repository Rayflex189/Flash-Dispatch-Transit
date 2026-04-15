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

# Create necessary directories
RUN mkdir -p static media staticfiles

# Run migrations (will be done in release command)
# RUN python manage.py migrate --noinput

# Collect static files
RUN python manage.py collectstatic --noinput

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /code
USER appuser

# Run the application with gunicorn
CMD ["gunicorn", "flash_dispatch.wsgi:application", "--bind", "0.0.0.0:8020", "--workers", "2", "--worker-class", "sync"]
