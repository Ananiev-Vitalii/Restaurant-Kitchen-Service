#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

# Loading fixture with data
python manage.py loaddata kitchen_service/fixtures/cooks.json
python manage.py loaddata kitchen_service/fixtures/ingredients.json
python manage.py loaddata kitchen_service/fixtures/dishtypes.json
python manage.py loaddata kitchen_service/fixtures/dishes.json
python manage.py loaddata kitchen_service/fixtures/orders.json
