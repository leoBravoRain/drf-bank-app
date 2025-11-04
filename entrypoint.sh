#!/bin/sh

echo "Waiting for PostgreSQL..."
while ! pg_isready -h db -p 5432 -U postgres; do
  sleep 1
done

echo "PostgreSQL is ready!"
python manage.py migrate
python manage.py collectstatic --noinput

exec "$@"

