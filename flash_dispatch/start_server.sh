#!/bin/bash

echo "🚀 Starting Flash Dispatch Server..."

# Check if running in Codespaces
if [ -n "$CODESPACES" ]; then
    echo "📡 Running in GitHub Codespaces"
    HOST="0.0.0.0"
    PORT="8000"
else
    HOST="127.0.0.1"
    PORT="8000"
fi

# Choose server type
echo ""
echo "Select server type:"
echo "1) Django Development Server (WSGI - Simple, auto-reload)"
echo "2) Gunicorn (WSGI - Production ready, faster)"
echo "3) Daphne (ASGI - Supports WebSockets, async)"
echo "4) Uvicorn (ASGI - Fast, modern)"
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo "🔧 Starting Django development server..."
        python manage.py runserver $HOST:$PORT
        ;;
    2)
        echo "🔧 Starting Gunicorn (WSGI)..."
        pip install gunicorn
        gunicorn flash_dispatch.wsgi:application --bind $HOST:$PORT --workers 4 --reload
        ;;
    3)
        echo "🔧 Starting Daphne (ASGI)..."
        pip install daphne
        daphne -b $HOST -p $PORT flash_dispatch.asgi:application
        ;;
    4)
        echo "🔧 Starting Uvicorn (ASGI)..."
        pip install uvicorn
        uvicorn flash_dispatch.asgi:application --host $HOST --port $PORT --reload
        ;;
    *)
        echo "Invalid choice. Starting Django development server..."
        python manage.py runserver $HOST:$PORT
        ;;
esac