#!/usr/bin/env bash
# exit on error
set -o errexit

# Install required backend libraries
pip install -r requirements.txt

# Compile static assets
python manage.py collectstatic --no-input

# Run database schema migrations
python manage.py makemigrations products orders payments core dashboard --no-input
python manage.py migrate

# Seed catalog database 
python manage.py seed_products
