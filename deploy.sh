#!/bin/bash

# Exit on error
set -e

echo "--- Starting Deployment Script ---"

# 1. Clear any old migration caches
find . -name "*.pyc" -delete
find . -name "__pycache__" -delete

# 2. Force create migrations for mpesa app
echo "Creating migrations..."
python3 manage.py makemigrations mpesa
python3 manage.py makemigrations loans

# 3. Apply migrations
echo "Applying migrations..."
python3 manage.py migrate --noinput

# 4. Seed data (includes your MegaPay credentials)
echo "Seeding data..."
python3 seed_data.py

# 5. Start the web server
echo "Starting Gunicorn..."
exec gunicorn talamkopo.wsgi --log-file -
