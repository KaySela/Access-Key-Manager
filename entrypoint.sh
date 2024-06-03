#!/bin/sh

# Wait for the database to be ready
while ! nc -z db 5432; do
  echo "waiting for database to be ready..."
  sleep 1
done

echo "Database is ready!"

# Run migrations and then start the server
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py createmicroadmin
gunicorn KeyManager.wsgi:application --bind 0.0.0.0:8000