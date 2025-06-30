#!/bin/sh

set -x

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate
echo "Done!"

echo "Creating a SU if not exists..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
  User.objects.create_superuser('admin', 'admin@exemple.com', 'admin')
  print('Superuser created!')
else:
  print('Superuser already exists.')
EOF

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000