#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input --settings=core.settings_prod

echo "Running migrations..."
python manage.py migrate --settings=core.settings_prod

echo "Seeding initial data to Cloud DB..."
python manage.py seed_data --settings=core.settings_prod