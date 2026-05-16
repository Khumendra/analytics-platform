#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations using production configurations 
python manage.py migrate --settings=core.settings_prod

# Collect static files (if any)
python manage.py collectstatic --no-input --settings=core.settings_prod

# Start Celery worker in the background dynamically
celery -A core worker --loglevel=info --pool=solo &